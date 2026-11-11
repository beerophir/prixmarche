from django.urls import path

from . import views

app_name = "prix"

urlpatterns = [
    path("", views.accueil, name="accueil"),

    path("produits/", views.produits, name="produits"),
    path("produits/nouveau/", views.produit_creer, name="produit_creer"),
    path("produits/<str:pk>/modifier/", views.produit_modifier, name="produit_modifier"),
    path("produits/<str:pk>/supprimer/", views.produit_supprimer, name="produit_supprimer"),

    path("marches/", views.marches, name="marches"),
    path("marches/nouveau/", views.marche_creer, name="marche_creer"),
    path("marches/<str:pk>/modifier/", views.marche_modifier, name="marche_modifier"),
    path("marches/<str:pk>/supprimer/", views.marche_supprimer, name="marche_supprimer"),

    path("enqueteurs/", views.enqueteurs, name="enqueteurs"),
    path("enqueteurs/nouveau/", views.enqueteur_creer, name="enqueteur_creer"),
    path("enqueteurs/<str:pk>/modifier/", views.enqueteur_modifier, name="enqueteur_modifier"),
    path("enqueteurs/<str:pk>/supprimer/", views.enqueteur_supprimer, name="enqueteur_supprimer"),

        path("affectations/", views.affectations, name="affectations"),
    path("affectations/nouvelle/", views.affectation_creer, name="affectation_creer"),
    path("affectations/<int:pk>/modifier/", views.affectation_modifier, name="affectation_modifier"),
    path("affectations/<int:pk>/supprimer/", views.affectation_supprimer, name="affectation_supprimer"),

    path("releves/", views.releves, name="releves"),
    path("releves/nouveau/", views.releve_creer, name="releve_creer"),
    path("releves/<int:pk>/", views.releve_detail, name="releve_detail"),
    path("releves/<int:pk>/modifier/", views.releve_modifier, name="releve_modifier"),
    path("releves/<int:pk>/supprimer/", views.releve_supprimer, name="releve_supprimer"),
]