"""
API Views for Chemical Equipment Parameter Visualizer.
"""
from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate
from django.http import HttpResponse

from .models import Equipment, UploadSession
from .serializers import (
    EquipmentSerializer, 
    UploadSessionSerializer, 
    SummarySerializer,
    LoginSerializer,
    UserSerializer,
    RegisterSerializer
)
from .utils import parse_csv, calculate_summary, generate_pdf_report


class LoginView(views.APIView):
    """Handle user login and token generation."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class RegisterView(views.APIView):
    """Handle user registration."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Registration successful',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(views.APIView):
    """Handle user logout by deleting token."""
    
    def post(self, request):
        if request.user.auth_token:
            request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'})


class UploadCSVView(views.APIView):
    """Handle CSV file upload and processing."""
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        if not file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be a CSV'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Parse CSV
            df = parse_csv(file)
            
            # Create upload session
            session = UploadSession.objects.create(
                user=request.user,
                filename=file.name,
                record_count=len(df)
            )
            
            # Create equipment records
            equipment_objects = []
            for _, row in df.iterrows():
                equipment_objects.append(Equipment(
                    session=session,
                    name=row['name'],
                    equipment_type=row['equipment_type'],
                    flowrate=row['flowrate'],
                    pressure=row['pressure'],
                    temperature=row['temperature']
                ))
            Equipment.objects.bulk_create(equipment_objects)
            
            # Calculate and store summary
            summary = calculate_summary(session.equipment.all())
            session.summary = summary
            session.save()
            
            # Cleanup old sessions (keep only last 5)
            UploadSession.cleanup_old_sessions(request.user)
            
            return Response({
                'message': 'File uploaded successfully',
                'session_id': session.id,
                'record_count': session.record_count,
                'summary': summary
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error processing file: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EquipmentListView(generics.ListAPIView):
    """List equipment from the latest upload session."""
    serializer_class = EquipmentSerializer
    
    def get_queryset(self):
        session_id = self.request.query_params.get('session_id')
        
        if session_id:
            return Equipment.objects.filter(
                session_id=session_id,
                session__user=self.request.user
            )
        
        # Get latest session
        latest_session = UploadSession.objects.filter(
            user=self.request.user
        ).first()
        
        if latest_session:
            return Equipment.objects.filter(session=latest_session)
        
        return Equipment.objects.none()


class SummaryView(views.APIView):
    """Get summary statistics for the latest or specified session."""
    
    def get(self, request):
        session_id = request.query_params.get('session_id')
        
        if session_id:
            try:
                session = UploadSession.objects.get(
                    id=session_id,
                    user=request.user
                )
            except UploadSession.DoesNotExist:
                return Response(
                    {'error': 'Session not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            session = UploadSession.objects.filter(user=request.user).first()
            
            if not session:
                # Return empty summary instead of 404
                return Response({
                    'session_id': None,
                    'filename': None,
                    'uploaded_at': None,
                    'total_count': 0,
                    'avg_flowrate': 0,
                    'avg_pressure': 0,
                    'avg_temperature': 0,
                    'min_flowrate': 0,
                    'max_flowrate': 0,
                    'type_distribution': {}
                })
        
        # Recalculate summary for accuracy
        summary = calculate_summary(session.equipment.all())
        
        return Response({
            'session_id': session.id,
            'filename': session.filename,
            'uploaded_at': session.uploaded_at,
            **summary
        })


class HistoryListView(generics.ListAPIView):
    """List last 5 upload sessions for the user."""
    serializer_class = UploadSessionSerializer
    
    def get_queryset(self):
        return UploadSession.objects.filter(
            user=self.request.user
        ).order_by('-uploaded_at')[:5]


class PDFReportView(views.APIView):
    """Generate and download PDF report."""
    
    def get(self, request):
        session_id = request.query_params.get('session_id')
        
        if session_id:
            try:
                session = UploadSession.objects.get(
                    id=session_id,
                    user=request.user
                )
            except UploadSession.DoesNotExist:
                return Response(
                    {'error': 'Session not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            session = UploadSession.objects.filter(user=request.user).first()
            
            if not session:
                return Response(
                    {'error': 'No upload sessions found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Get equipment and summary
        equipment_list = list(session.equipment.all())
        summary = calculate_summary(session.equipment.all())
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(session, equipment_list, summary)
        
        # Return PDF response
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{session.id}.pdf"'
        
        return response
