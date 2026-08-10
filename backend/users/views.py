from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, PredictionSerializer, DiseaseSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, filters, generics, permissions
from users.models import NewUser, Disease, Prediction
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import tensorflow as tf
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend



import cv2 as cv
import numpy as np
from django.core.files.base import ContentFile


class CustomUserCreate(APIView):

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BlacklistTokenUpdateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetUserView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serialized_user = CustomUserSerializer(context={'request': request})
        return Response(serialized_user.data)




class UserDetail(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserSerializer
    queryset = NewUser.objects.all()

    def get(self, request, *args, **kwargs):
        user_count = self.get_queryset().count()
        data = {
            'user_count': user_count,
        }
        return Response(data)



from rest_framework import generics
from .models import Prediction
from .serializers import PredictionSerializer

class PostList(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PredictionSerializer
    queryset = Prediction.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        predictions = self.queryset.prefetch_related('diseases')  # Prefetch diseases to reduce DB queries
        diseases_summary = {prediction.id: prediction.get_diseases_summary() for prediction in predictions}
        context['diseases_summary'] = diseases_summary
        return context




class DeseaseDetail(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = DiseaseSerializer
    queryset = Disease.objects.all()


    def get(self, request, *args, **kwargs):
        desease_count = self.get_queryset().count()

        data = {
            'desease_count': desease_count,
        
        }
        return Response(data)




class PostDetail(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = DiseaseSerializer

    def get_queryset(self):
        return Disease.objects.all()


class Post(generics.RetrieveAPIView):
    serializer_class = PredictionSerializer

    def get_queryset(self):
        return Prediction.objects.all()
    


class DiseaseDetail(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = DiseaseSerializer

    def get_object(self, queryset=None, **kwargs):
        item_image_name = self.kwargs.get('pk')  # Use 'imageName' here
        return get_object_or_404(Disease, name=item_image_name)





class PredictionDetail(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PredictionSerializer
    queryset = Prediction.objects.all()
    # print(queryset)

    def get(self, request, *args, **kwargs):
        prediction_count = self.get_queryset().count()
        data = {
            'prediction_count': prediction_count,
        }
        return Response(data)






class PredictionList(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = DiseaseSerializer
    queryset = Disease.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['diseases__id']  # Allow filtering by disease name

    def get_queryset(self):
        queryset = super().get_queryset()
        disease_name = self.request.query_params.get('diseases__id')
        if disease_name:
            queryset = queryset.filter(diseases__name=disease_name)
        return queryset

    



interpreter = tf.lite.Interpreter(
    model_path="models/coffee_leaf_binary_network_efficientnetv2_b0_adam0_0003_batch128.tflite"
)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
segmentationModel = tf.keras.models.load_model(
    "models/segmentation_model.h5", compile=False
)

classificationModel = tf.keras.models.load_model("models/class_new_5.h5", compile=False)

leafSegmentationModel = tf.keras.models.load_model(
    "models/leaf_segmentation.h5", compile=False
)

DISEASE_NAMES = ["free_feeder", "leaf_rust", "leaf_skeletonizer"]

COLORS = [(0, 0, 255), (255, 0, 0), (100, 100, 0)]



class PredictionView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [permissions.IsAuthenticated]


    def post(self, request, format=None):
        data = request.data
        # user = request.user if request.user.is_authenticated else None
        requestImage = data["image"]
        image = self.grab_image(stream=request.FILES["image"])
        imageSize = image.shape[:2]
        imageName = data["imageName"]
        scanned = True if data.get("scanned") and data.get(
            "scanned").lower() == "true" else False

        verificationImage = cv.resize(image, (224, 224))
        verificationImage = np.reshape(verificationImage, (1, 224, 224, 3))
        input_data = np.array(verificationImage, dtype=np.float32)
        interpreter.set_tensor(input_details[0]["index"], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(
            output_details[0]["index"])[0][0]
        if output_data > 0.2:
            return Response("invalid image", status=400)

        rotated = False
        if image.shape[0] > image.shape[1]:
            image = cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE)
            rotated = True

        image = cv.resize(image, (512, 512))
        imageName = 'leaf'
        predictedImage, predictedDiseases, severity = self.segmentImage(
            image=image)
        prediction = Prediction(
            imageName=imageName,
            scanned=scanned,
            image=requestImage,
            severity=severity,

        )
        prediction.save()

        if rotated:
            predictedImage = cv.rotate(predictedImage, cv.ROTATE_90_CLOCKWISE)

        predictedImage = cv.resize(predictedImage, imageSize[::-1])
        ret, buf = cv.imencode(".jpg", predictedImage)
        content = ContentFile(buf.tobytes())
        prediction.predictedImage.save(imageName, content)

        disease_objects = []

        for disease_name in predictedDiseases:
            # Get or create the Disease object based on the disease_name
            disease, created = Disease.objects.get_or_create(name=disease_name)
            disease_objects.append(disease)

        for disease in disease_objects:
            # Add the Disease object to the prediction's diseases
            prediction.diseases.add(disease)

        serializer = PredictionSerializer(prediction)
        return Response(serializer.data)

    def grab_image(self, stream):
        data = stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv.imdecode(image, cv.IMREAD_COLOR)
        return image

    def segmentImage(self, image):
        segmentation = segmentationModel.predict(np.array([image]))
        segmentation = segmentation[0]
        segmentation = np.amax(segmentation, axis=-1)
        segmentation[segmentation >= 0.5] = 1
        segmentation[segmentation < 0.5] = 0
        segmentation = segmentation * 255
        currDiseases = set()
        segmentation = np.array(segmentation, np.uint8)
        contours, hierarchy = cv.findContours(
            segmentation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )

        if contours:
            leafMask = leafSegmentationModel.predict(np.array([image]))[0]
            leafMask = leafMask >= 0.5
            leafArea = np.sum(leafMask)
            maskArea = segmentation == 255
            diseasedArea = np.sum(maskArea)
            severity = diseasedArea / (leafArea - diseasedArea)
        else:
            severity = 0

        originalImage = image.copy()

        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            croppedImage = image[y: y + h, x: x + w]

            if w < 7 or h < 7:
                continue

            croppedImage = cv.resize(croppedImage, (150, 150))
            output = classificationModel.predict(
                np.array([croppedImage]))[0]
            diseaseIndex = max(list(range(len(output))),
                               key=lambda x: output[x])
            currDisease = DISEASE_NAMES[diseaseIndex]
            thickness = 5
            cv.drawContours(image, [cnt], 0,
                            COLORS[diseaseIndex], -thickness)
            cv.fillConvexPoly(image, cnt, COLORS[diseaseIndex])
            currDiseases.add(currDisease)

        predictedImage = cv.addWeighted(originalImage, 0.6, image, 0.4, 0)

        return predictedImage, list(currDiseases), severity


class AllDataView(APIView):
    def get(self, request, format=None):
        predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)
