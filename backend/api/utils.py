"""
Utility functions for data analysis and PDF generation.
"""
import io
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch


def parse_csv(file):
    """
    Parse uploaded CSV file and return DataFrame.
    
    Expected columns: Equipment Name, Type, Flowrate, Pressure, Temperature
    """
    df = pd.read_csv(file)
    
    # Standardize column names
    column_mapping = {
        'Equipment Name': 'name',
        'Type': 'equipment_type',
        'Flowrate': 'flowrate',
        'Pressure': 'pressure',
        'Temperature': 'temperature'
    }
    
    # Rename columns that exist
    for old_name, new_name in column_mapping.items():
        if old_name in df.columns:
            df = df.rename(columns={old_name: new_name})
    
    # Validate required columns
    required_cols = ['name', 'equipment_type', 'flowrate', 'pressure', 'temperature']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    
    # Convert numeric columns
    df['flowrate'] = pd.to_numeric(df['flowrate'], errors='coerce')
    df['pressure'] = pd.to_numeric(df['pressure'], errors='coerce')
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    
    # Drop rows with NaN values
    df = df.dropna(subset=['flowrate', 'pressure', 'temperature'])
    
    return df


def calculate_summary(equipment_queryset):
    """
    Calculate summary statistics from an equipment queryset.
    """
    if not equipment_queryset.exists():
        return {
            'total_count': 0,
            'avg_flowrate': 0,
            'avg_pressure': 0,
            'avg_temperature': 0,
            'min_flowrate': 0,
            'max_flowrate': 0,
            'min_pressure': 0,
            'max_pressure': 0,
            'min_temperature': 0,
            'max_temperature': 0,
            'type_distribution': {}
        }
    
    # Get all values
    flowrates = list(equipment_queryset.values_list('flowrate', flat=True))
    pressures = list(equipment_queryset.values_list('pressure', flat=True))
    temperatures = list(equipment_queryset.values_list('temperature', flat=True))
    
    # Type distribution
    type_counts = {}
    for eq in equipment_queryset.values('equipment_type'):
        eq_type = eq['equipment_type']
        type_counts[eq_type] = type_counts.get(eq_type, 0) + 1
    
    return {
        'total_count': len(flowrates),
        'avg_flowrate': round(sum(flowrates) / len(flowrates), 2),
        'avg_pressure': round(sum(pressures) / len(pressures), 2),
        'avg_temperature': round(sum(temperatures) / len(temperatures), 2),
        'min_flowrate': round(min(flowrates), 2),
        'max_flowrate': round(max(flowrates), 2),
        'min_pressure': round(min(pressures), 2),
        'max_pressure': round(max(pressures), 2),
        'min_temperature': round(min(temperatures), 2),
        'max_temperature': round(max(temperatures), 2),
        'type_distribution': type_counts
    }


def generate_pdf_report(session, equipment_list, summary):
    """
    Generate a PDF report for the upload session.
    Returns a bytes buffer.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=10
    )
    
    elements = []
    
    # Title
    elements.append(Paragraph("Chemical Equipment Parameter Report", title_style))
    elements.append(Spacer(1, 12))
    
    # File info
    elements.append(Paragraph(f"<b>File:</b> {session.filename}", styles['Normal']))
    elements.append(Paragraph(f"<b>Uploaded:</b> {session.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Paragraph(f"<b>Total Records:</b> {summary['total_count']}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Summary Statistics
    elements.append(Paragraph("Summary Statistics", heading_style))
    
    summary_data = [
        ['Metric', 'Flowrate', 'Pressure', 'Temperature'],
        ['Average', str(summary['avg_flowrate']), str(summary['avg_pressure']), str(summary['avg_temperature'])],
        ['Minimum', str(summary['min_flowrate']), str(summary['min_pressure']), str(summary['min_temperature'])],
        ['Maximum', str(summary['max_flowrate']), str(summary['max_pressure']), str(summary['max_temperature'])],
    ]
    
    summary_table = Table(summary_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Type Distribution
    elements.append(Paragraph("Equipment Type Distribution", heading_style))
    
    type_data = [['Type', 'Count']]
    for eq_type, count in summary['type_distribution'].items():
        type_data.append([eq_type, str(count)])
    
    type_table = Table(type_data, colWidths=[3*inch, 1.5*inch])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1fae5')),
    ]))
    elements.append(type_table)
    elements.append(Spacer(1, 20))
    
    # Equipment Data Table
    elements.append(Paragraph("Equipment Data", heading_style))
    
    eq_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
    for eq in equipment_list[:50]:  # Limit to 50 rows for PDF
        eq_data.append([
            eq.name,
            eq.equipment_type,
            str(eq.flowrate),
            str(eq.pressure),
            str(eq.temperature)
        ])
    
    eq_table = Table(eq_data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 1*inch, 1.2*inch])
    eq_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#faf5ff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e9d5ff')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#faf5ff')]),
    ]))
    elements.append(eq_table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
