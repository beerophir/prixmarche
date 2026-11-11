from datetime import date
from django import forms

from .models import Affectation, Enqueteur, Marche, Produit, Releve

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ["code_produit", "libelle", "unite"]


class MarcheForm(forms.ModelForm):
    class Meta:
        model = Marche
        fields = ["code_marche", "nom_marche", "ville"]


class EnqueteurForm(forms.ModelForm):
    class Meta:
        model = Enqueteur
        fields = ["matricule", "nom_enq", "telephone"]


class AffectationForm(forms.ModelForm):
    class Meta:
        model = Affectation
        fields = ["enqueteur", "marche", "date_debut"]
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date"}),
        }

class ReleveForm(forms.ModelForm):
    class Meta:
        model = Releve
        fields = ["date_releve", "prix", "produit", "marche", "enqueteur"]
        labels = {"prix": "Prix observé (FCFA)"}
        widgets = {
            "date_releve": forms.DateInput(attrs={"type": "date"}),
            "prix": forms.NumberInput(attrs={"min": 1, "inputmode": "numeric"}),
        }

    def clean_date_releve(self):
        """Un relevé constate un prix observé : il ne peut pas être daté du futur."""
        valeur = self.cleaned_data["date_releve"]
        if valeur > date.today():
            raise forms.ValidationError("La date du relevé ne peut pas être future.")
        return valeur

    def clean_prix(self):
        """Le prix doit être strictement positif."""
        valeur = self.cleaned_data["prix"]
        if valeur <= 0:
            raise forms.ValidationError("Le prix doit être strictement positif.")
        return valeur

    def clean(self):
        """Un enquêteur ne relève que sur un marché auquel il est affecté."""
        donnees = super().clean()
        enqueteur = donnees.get("enqueteur")
        marche = donnees.get("marche")
        if enqueteur and marche:
            affecte = Affectation.objects.filter(
                enqueteur=enqueteur, marche=marche
            ).exists()
            if not affecte:
                self.add_error("marche", "Cet enquêteur n'est pas affecté à ce marché.")
        return donnees
    