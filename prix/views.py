from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AffectationForm, EnqueteurForm, MarcheForm, ProduitForm, ReleveForm
from .models import Affectation, Enqueteur, Marche, Produit, Releve


def accueil(request):
    """Page d'accueil : mini tableau de bord de l'observatoire."""
    compteurs = {
        "produits": Produit.objects.count(),
        "marches": Marche.objects.count(),
        "enqueteurs": Enqueteur.objects.count(),
        "affectations": Affectation.objects.count(),
        "releves": Releve.objects.count(),
    }
    return render(request, "prix/accueil.html", {"compteurs": compteurs})


# ---------------------------------------------------------------- Produits

def produits(request):
    lignes = Produit.objects.order_by("libelle")
    return render(request, "prix/produits.html", {"lignes": lignes})


def produit_creer(request):
    form = ProduitForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Produit créé.")
        return redirect("prix:produits")
    return render(request, "prix/formulaire.html", {
        "form": form, "titre": "Nouveau produit", "retour": "prix:produits",
    })


def produit_modifier(request, pk):
    objet = get_object_or_404(Produit, pk=pk)
    form = ProduitForm(request.POST or None, instance=objet)
    form.fields["code_produit"].disabled = True
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Produit modifié.")
        return redirect("prix:produits")
    return render(request, "prix/formulaire.html", {
        "form": form, "titre": "Modifier le produit", "retour": "prix:produits",
    })


def produit_supprimer(request, pk):
    objet = get_object_or_404(Produit, pk=pk)
    if request.method == "POST":
        try:
            objet.delete()
        except ProtectedError:
            messages.error(request, "Suppression impossible : ce produit est utilisé par des relevés.")
        else:
            messages.success(request, "Produit supprimé.")
        return redirect("prix:produits")
    return render(request, "prix/confirmer_suppression.html", {
        "objet": objet, "titre": "Supprimer le produit", "retour": "prix:produits",
    })


# ---------------------------------------------------------------- Marchés

def marches(request):
    lignes = Marche.objects.order_by("nom_marche")
    return render(request, "prix/marches.html", {"lignes": lignes})


def marche_creer(request):
    form = MarcheForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Marché créé.")
        return redirect("prix:marches")
    return render(request, "prix/formulaire.html", {
        "form": form, "titre": "Nouveau marché", "retour": "prix:marches",
    })


def marche_modifier(request, pk):
    objet = get_object_or_404(Marche, pk=pk)
    form = MarcheForm(request.POST or None, instance=objet)
    form.fields["code_marche"].disabled = True
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Marché modifié.")
        return redirect("prix:marches")
    return render(request, "prix/formulaire.html", {
        "form": form, "titre": "Modifier le marché", "retour": "prix:marches",
    })


def marche_supprimer(request, pk):
    objet = get_object_or_404(Marche, pk=pk)
    if request.method == "POST":
        try:
            objet.delete()
        except ProtectedError:
            messages.error(request, "Suppression impossible : ce marché est utilisé par des affectations ou des relevés.")
        else:
            messages.success(request, "Marché supprimé.")
        return redirect("prix:marches")
    return render(request, "prix/confirmer_suppression.html", {
        "objet": objet, "titre": "Supprimer le marché", "retour": "prix:marches",
    })


# ---------------------------------------------------------------- Enquêteurs

def enqueteurs(request):
    lignes = Enqueteur.objects.order_by("nom_enq")
    return render(request, "prix/enqueteurs.html", {"lignes": lignes})


def enqueteur_creer(request):
    form = EnqueteurForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Enquêteur créé.")
        return redirect("prix:enqueteurs")
    return render(request, "prix/formulaire.html", {
        "form": form, "titre": "Nouvel enquêteur", "retour": "prix:enqueteurs",
    })


def enqueteur_modifier(request, pk):
    objet = get_object_or_404(Enqueteur, pk=pk)
    form = EnqueteurForm(request.POST or None, instance=objet)
    form.fields["matricule"].disabled = True
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Enquêteur modifié.")
        return redirect("prix:enqueteurs")
    return render(request, "prix/formulaire.html", {
        "form": form, "titre": "Modifier l'enquêteur", "retour": "prix:enqueteurs",
    })


def enqueteur_supprimer(request, pk):
    objet = get_object_or_404(Enqueteur, pk=pk)
    if request.method == "POST":
        try:
            objet.delete()
        except ProtectedError:
            messages.error(request, "Suppression impossible : cet enquêteur a des affectations ou des relevés.")
        else:
            messages.success(request, "Enquêteur supprimé.")
        return redirect("prix:enqueteurs")
    return render(request, "prix/confirmer_suppression.html", {
        "objet": objet, "titre": "Supprimer l'enquêteur", "retour": "prix:enqueteurs",
    })
# ---------------------------------------------------------------- Affectations

def affectations(request):
    lignes = (Affectation.objects
              .select_related("enqueteur", "marche")
              .order_by("-date_debut"))
    return render(request, "prix/affectations.html", {"lignes": lignes})


def affectation_creer(request):
    form = AffectationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Affectation créée.")
        return redirect("prix:affectations")
    return render(request, "prix/formulaire.html", {
        "form": form, "titre": "Nouvelle affectation", "retour": "prix:affectations",
    })


def affectation_modifier(request, pk):
    objet = get_object_or_404(Affectation, pk=pk)
    form = AffectationForm(request.POST or None, instance=objet)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Affectation modifiée.")
        return redirect("prix:affectations")
    return render(request, "prix/formulaire.html", {
        "form": form, "titre": "Modifier l'affectation", "retour": "prix:affectations",
    })


def affectation_supprimer(request, pk):
    objet = get_object_or_404(Affectation, pk=pk)
    if request.method == "POST":
        objet.delete()
        messages.success(request, "Affectation supprimée.")
        return redirect("prix:affectations")
    return render(request, "prix/confirmer_suppression.html", {
        "objet": objet, "titre": "Supprimer l'affectation", "retour": "prix:affectations",
    })

# ---------------------------------------------------------------- Relevés

def releves(request):
    lignes = (Releve.objects
              .select_related("produit", "marche", "enqueteur")
              .order_by("-date_releve", "-num_releve"))
    return render(request, "prix/releves.html", {"lignes": lignes})


def releve_detail(request, pk):
    releve = get_object_or_404(
        Releve.objects.select_related("produit", "marche", "enqueteur"), pk=pk
    )
    return render(request, "prix/releve_detail.html", {"releve": releve})


def releve_creer(request):
    form = ReleveForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        releve = form.save()
        messages.success(request, f"Relevé n° {releve.pk} enregistré.")
        return redirect("prix:releves")
    return render(request, "prix/formulaire.html", {
        "form": form, "titre": "Nouveau relevé", "retour": "prix:releves",
    })


def releve_modifier(request, pk):
    objet = get_object_or_404(Releve, pk=pk)
    form = ReleveForm(request.POST or None, instance=objet)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Relevé corrigé.")
        return redirect("prix:releve_detail", pk=objet.pk)
    return render(request, "prix/formulaire.html", {
        "form": form, "titre": f"Modifier le relevé n° {objet.pk}", "retour": "prix:releves",
    })


def releve_supprimer(request, pk):
    objet = get_object_or_404(Releve, pk=pk)
    if request.method == "POST":
        objet.delete()
        messages.success(request, "Relevé supprimé.")
        return redirect("prix:releves")
    return render(request, "prix/confirmer_suppression.html", {
        "objet": objet, "titre": "Supprimer le relevé", "retour": "prix:releves",
    })