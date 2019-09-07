from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from . import serializers as serializers
from . import models as models


class CompanyViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CompanySerializer

    def get_queryset(self):
        return models.Company \
            .objects \
            .filter(users=self.request.user) \
            .order_by('-created')

    def perform_create(self, serializer):
        company = serializer.save()

        company.users.add(self.request.user)


class UnitOfMeasurementViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UnitOfMeasurementSerializer

    def get_queryset(self):
        return models.UnitOfMeasurement \
            .objects \
            .filter(product__company__user=self.request.user, product=self.kwargs['products_pk']) \
            .order_by('-created')

    def perform_create(self, serializer):
        product = models.Product \
            .objects \
            .get(company__user=self.request.user, pk=self.kwargs['products_pk'])
        serializer.save(product=product)


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        return models.Product \
            .objects \
            .filter(company__users=self.request.user, company=self.kwargs['companies_pk']) \
            .order_by('-created')

    def perform_create(self, serializer):
        serializer.save(company=models.Company.objects.get(users=self.request.user, pk=self.kwargs['companies_pk']))


class ProductionLineViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProductionLineSerializer

    def get_queryset(self):
        return models.ProductionLine \
            .objects \
            .filter(company__user=self.request.user, company=self.kwargs['companies_pk']) \
            .order_by('-created')


class TurnSchemeViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TurnSchemeSerializer

    def get_queryset(self):
        return models.TurnScheme. \
            objects. \
            filter(company__user=self.request.user, company=self.kwargs['companies_pk']). \
            order_by('-created')

    def perform_create(self, serializer):
        serializer.save(company=models.Company.objects.get(users=self.request.user, pk=self.kwargs['companies_pk']))


class TurnViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TurnSerializer

    def get_queryset(self):
        return models.Turn \
            .objects \
            .filter(turn_scheme__company__user=self.request.user, turn_scheme=self.kwargs['turn_schemes_pk']) \
            .order_by('-created')

    def perform_create(self, serializer):
        turn_scheme = models.TurnScheme \
            .objects \
            .get(company__user=self.request.user, pk=self.kwargs['turn_schemes_pk'])
        serializer.save(turn_scheme=turn_scheme)
