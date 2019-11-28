import graphene
from graphql_jwt.decorators import login_required
from django.db.models import Q
from .models import *


class PromocodeObj(graphene.ObjectType):
    code = graphene.String()
    description = graphene.String()


class ProductDetailObj(graphene.ObjectType):
    name = graphene.String()
    photo = graphene.String()
    fee = graphene.Int()


class ProductObj(graphene.ObjectType):
    isAvailable = graphene.String()
    productID = graphene.String()
    product = graphene.Field(ProductDetailObj)

    def resolve_product(self, info):
        product = Product.objects.get(productID=self['productID']).product
        photo = None
        if product.cover is not None:
            photo = info.context.build_absolute_uri(product.cover.url)
        return {"name": product.name, "photo": photo, "price": product.fee}


class Query(object):
    listPromocodes = graphene.List(PromocodeObj)
    getProduct = graphene.Field(ProductObj, productID=graphene.String(required=True))

    @login_required
    def resolve_listPromocodes(self, info, **kwargs):
        user = info.context.user
        return PromoCode.objects.values().filter(Q(users=user) | Q(users=None))

    @login_required
    def resolve_getProduct(self, info, **kwargs):
        productID = kwargs.get('productID')
        return Product.objects.values().get(productID=productID)
