from django.contrib import admin

from .models import Affectation, Enqueteur, Marche, Produit, Releve


@admin.register(Marche)
class MarcheAdmin(admin.ModelAdmin):
    list_display = ("code_marche", "nom_marche", "ville")
    search_fields = ("nom_marche", "ville")


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ("code_produit", "libelle", "unite")
    list_filter = ("unite",)
    search_fields = ("libelle",)


@admin.register(Enqueteur)
class EnqueteurAdmin(admin.ModelAdmin):
    list_display = ("matricule", "nom_enq", "telephone")
    search_fields = ("matricule", "nom_enq")


@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ("enqueteur", "marche", "date_debut")


@admin.register(Releve)
class ReleveAdmin(admin.ModelAdmin):
    list_display = (
        "num_releve", "date_releve", "marche",
        "produit", "prix", "enqueteur",
    )
    list_filter = ("date_releve", "marche", "produit")