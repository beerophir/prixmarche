from django.db import models


class Marche(models.Model):
    """Un marché suivi par l'observatoire."""

    code_marche = models.CharField(max_length=10, primary_key=True)
    nom_marche = models.CharField(max_length=80)
    ville = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.nom_marche} ({self.ville})"


class Produit(models.Model):
    """Un produit vivrier et son unité de mesure."""

    UNITES = [
        ("tas", "Tas"),
        ("regime", "Régime"),
        ("kg", "Kilogramme"),
    ]

    code_produit = models.CharField(max_length=6, primary_key=True)
    libelle = models.CharField(max_length=60)
    unite = models.CharField(max_length=6, choices=UNITES)

    def __str__(self):
        return f"{self.libelle} ({self.get_unite_display()})"


class Enqueteur(models.Model):
    """Un agent qui relève les prix sur le terrain."""

    matricule = models.CharField(max_length=8, primary_key=True)
    nom_enq = models.CharField(max_length=60)
    telephone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.matricule} - {self.nom_enq}"


class Affectation(models.Model):
    """Association n-n : un enquêteur affecté à un marché, avec sa date de début."""

    enqueteur = models.ForeignKey(Enqueteur, on_delete=models.PROTECT)
    marche = models.ForeignKey(Marche, on_delete=models.PROTECT)
    date_debut = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["enqueteur", "marche"],
                name="uniq_enqueteur_marche",
            )
        ]

    def __str__(self):
        return f"{self.enqueteur} - {self.marche}"


class Releve(models.Model):
    """Un prix observé pour un produit, sur un marché, par un enquêteur."""

    num_releve = models.AutoField(primary_key=True)
    date_releve = models.DateField()
    prix = models.PositiveIntegerField()
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    marche = models.ForeignKey(Marche, on_delete=models.PROTECT)
    enqueteur = models.ForeignKey(Enqueteur, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.produit} - {self.marche} : {self.prix} FCFA"