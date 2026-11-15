# EVE FINALE - PARTIE 1 / 4 - COPIE CELLE-LA D'ABORD
import os, random, math, wave, struct
DOSSIER_FACEBOOK = "/storage/emulated/0/Pictures/Facebook"
try:
    DOSSIER_CODE = os.path.dirname(os.path.abspath(__file__))
except:
    DOSSIER_CODE = os.getcwd()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
Window.clearcolor = (0, 0, 0, 1)

PHOTO_FACADE = "Facebook_creation_1424243679752497.jpeg"
PHOTO_ACCUEIL = "Facebook_creation_1617790580092081.jpeg"
PHOTO_FAUTEUIL = "Facebook_creation_1904604204238664.jpeg"
PHOTO_DISCUSSION = "Facebook_creation_2380618709441336.jpeg"
PHOTO_CARNET = "Facebook_creation_1041633978951059.jpeg"
PHOTO_PORTE = "Facebook_creation_1680595863415907.jpeg"

messages = []
total_booms = 0
total_respirations = 0
total_quizz = 0

PHRASES_ENCOURAGEMENT = [
    "Bravo ! Tu es trop forte !",
    "Super ! Encore une !",
    "POC ! Tu fais partir la tristesse !",
    "Allez, tu peux le faire !",
    "Continue, tu te liberes !",
    "Oui ! Tu es courageuse !",
    "Encore ! Ca fait du bien, hein ?",
    "Bravo, tu fais partir la colere !",
    "Super ! Tu te sens plus legere ?",
    "Allez, encore une emotion qui part !",
    "Tu es incroyable, continue !",
    "POC ! Tu as bien fait !",
]

PHRASES_ENCOURAGEMENT_RESPIRATION = [
    "Allez, respire avec moi, tu peux le faire !",
    "Bravo ! Tu respires super bien !",
    "Continue, tu te calmes, c'est super !",
    "Tu es trop forte, encore une !",
    "Oui ! Tu sens comme ca fait du bien ?",
    "Allez, doucement, je suis avec toi !",
    "Bravo, ton coeur bat moins vite !",
    "Super ! Tu es en train de te calmer !",
    "Continue, tu fais ca tres bien !",
    "Je suis fiere de toi, respire !",
]

PHRASES_ENCOURAGEMENT_QUIZZ = [
    "Bravo ! Bonne reponse !",
    "Super ! Tu as tout compris !",
    "Oui ! C'est exactement ca !",
    "Bravo, tu es trop forte !",
    "Super ! Tu apprends vite !",
    "Oui ! Eve est fiere de toi !",
]

QUESTIONS_QUIZZ = [
    ("C'est quoi l'anxiete ?", ["Avoir peur de tout", "Se sentir stresse, le coeur qui bat vite", "Etre fatigue"], 1, "Oui ! L'anxiete c'est quand on est stresse, le coeur bat vite. C'est normal, ca arrive a tout le monde."),
    ("C'est quoi la tristesse ?", ["Etre en colere", "Se sentir mal, avoir envie de pleurer", "Avoir faim"], 1, "Oui ! La tristesse c'est se sentir mal, avoir envie de pleurer. Tu as le droit d'etre triste."),
    ("C'est quoi le stress ?", ["Etre content", "Se sentir tendu, comme si c'etait trop", "Avoir sommeil"], 1, "Oui ! Le stress c'est se sentir tendu, comme si c'etait trop. Respirer ca aide beaucoup."),
    ("Quand on est fatigue, qu'est-ce qu'il faut faire ?", ["Courir", "Se reposer, dormir, boire de l'eau", "Crier"], 1, "Oui ! Quand on est fatigue, il faut se reposer, dormir, boire de l'eau. Ton corps a besoin de repos."),
    ("C'est quoi la colere ?", ["Etre triste", "Etre content", "Se sentir enerve parce que quelque chose nous a fait mal"], 2, "Oui ! La colere c'est se sentir enerve parce que quelque chose nous a fait mal. Tu as le droit d'etre en colere."),
]

def creer_son(nom_fichier, type_son, duree):
    try:
        chemin = os.path.join(DOSSIER_CODE, nom_fichier)
        if os.path.exists(chemin):
            try:
                os.remove(chemin)
            except:
                pass
        taux = 22050
        nb = int(taux * duree)
        with wave.open(chemin, 'w') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(taux)
            for i in range(nb):
                t = i / taux
                if type_son == "inspire":
                    fondu = min(i / (taux * 0.3), (nb - i) / (taux * 0.3), 1.0)
                    fondu = max(0, fondu)
                    freq = 300 + (600 - 300) * (i / nb)
                    val = int(12000 * fondu * math.sin(2 * math.pi * freq * t))
                elif type_son == "expire":
                    fondu = min(i / (taux * 0.3), (nb - i) / (taux * 0.3), 1.0)
                    fondu = max(0, fondu)
                    freq = 600 - (600 - 300) * (i / nb)
                    val = int(12000 * fondu * math.sin(2 * math.pi * freq * t))
                else:
                    enveloppe = math.exp(-t * 35)
                    bruit = random.uniform(-1, 1)
                    clic = 0
                    if i < 200:
                        clic = math.sin(2 * math.pi * 2500 * t) * (1 - i / 200)
                    val = int(28000 * enveloppe * bruit + 8000 * enveloppe * clic)
                    if val > 30000:
                        val = 30000
                    if val < -30000:
                        val = -30000
                w.writeframes(struct.pack('<h', val))
        return chemin
    except:
        return None

# NOUVEAU : VRAIS cris de zombie, beaucoup plus realiste
# Si tu mets un fichier zombies_reel.mp3 a cote du code, on utilise celui-la, c'est encore mieux
def trouver_zombie_reel():
    for nom in ["zombies_reel.mp3", "zombies_reel.wav", "zombie.mp3", "zombie.wav", "zombies.mp3"]:
        for base in [DOSSIER_CODE, DOSSIER_FACEBOOK, os.getcwd()]:
            p = os.path.join(base, nom)
            if os.path.exists(p):
                return p
    return None

def creer_son_zombies(nom_fichier, duree=12.0):
    try:
        chemin = os.path.join(DOSSIER_CODE, nom_fichier)
        if os.path.exists(chemin):
            try:
                os.remove(chemin)
            except:
                pass
        taux = 22050
        nb = int(taux * duree)
        # 5 zombies qui crient vraiment : cris aigus + grognements graves
        # (debut, duree, freq debut, freq fin, volume, type)
        zombies = [
            (0.1, 2.5, 280, 90, 1.0, "cri"),
            (1.2, 2.8, 70, 160, 0.9, "grognement"),
            (3.0, 2.2, 320, 120, 1.0, "cri"),
            (4.8, 3.0, 85, 60, 0.9, "grognement"),
            (6.5, 2.6, 260, 80, 1.0, "cri"),
            (8.2, 3.0, 95, 180, 0.85, "grognement"),
            (10.0, 1.8, 350, 100, 0.9, "cri"),
        ]
        with wave.open(chemin, 'w') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(taux)
            for i in range(nb):
                t = i / taux
                val_total = 0
                for debut, duree_z, f1, f2, vol, typ in zombies:
                    if debut <= t < debut + duree_z:
                        tt = t - debut
                        progres = tt / duree_z
                        # Le cri monte tres fort puis redescend, comme un vrai cri
                        if progres < 0.2:
                            fondu = progres / 0.2
                        elif progres > 0.75:
                            fondu = (1.0 - progres) / 0.25
                        else:
                            fondu = 1.0
                        fondu = max(0, min(1, fondu))
                        # Tremblement de la voix, comme quand on crie vraiment
                        vibrato = 18 * math.sin(2 * math.pi * 9 * tt) + 8 * math.sin(2 * math.pi * 23 * tt)
                        freq = f1 + (f2 - f1) * progres + vibrato
                        if freq < 40:
                            freq = 40
                        # Voix rauque : plusieurs harmoniques + saturation
                        voix = math.sin(2 * math.pi * freq * tt) * 0.6
                        voix += math.sin(2 * math.pi * freq * 1.5 * tt + 0.5) * 0.35
                        voix += math.sin(2 * math.pi * freq * 2.0 * tt) * 0.25
                        # Rauque : on ecrase un peu le son, comme une gorge de zombie
                        if voix > 0.7:
                            voix = 0.7 + (voix - 0.7) * 0.3
                        if voix < -0.7:
                            voix = -0.7 + (voix + 0.7) * 0.3
                        bruit = random.uniform(-0.25, 0.25)
                        # Pour les cris, on met plus de souffle
                        if typ == "cri":
                            voix = voix * 1.2 + bruit * 0.4
                        else:
                            voix = voix + bruit * 0.2
                        val_total += voix * 11000 * fondu * vol
                # Vent + pas lourds en fond, comme des zombies qui marchent
                vent = math.sin(2 * math.pi * 40 * t) * 500
                pas = 0
                # Un pas lourd toutes les 1.2 secondes
                if (t % 1.2) < 0.08:
                    pas = math.sin(2 * math.pi * 55 * t) * 2500 * (1 - (t % 1.2) / 0.08)
                val_total += vent + pas
                if val_total > 30000:
                    val_total = 30000
                if val_total < -30000:
                    val_total = -30000
                w.writeframes(struct.pack('<h', int(val_total)))
        return chemin
    except:
        return None

CHEMIN_BOOM = creer_son("boom_eve.wav", "boom", 0.25)
CHEMIN_INSPIRE = creer_son("inspire_eve.wav", "inspire", 4.0)
CHEMIN_EXPIRE = creer_son("expire_eve.wav", "expire", 5.0)
CHEMIN_ZOMBIES = creer_son_zombies("zombies_eve.wav", 12.0)

son_actuel = None
son_zombie = None
def jouer_son(chemin):
    global son_actuel
    try:
        if son_actuel:
            try:
                son_actuel.stop()
            except:
                pass
        if chemin and os.path.exists(chemin):
            son_actuel = SoundLoader.load(chemin)
            if son_actuel:
                son_actuel.play()
    except:
        pass

def arreter_son():
    global son_actuel
    try:
        if son_actuel:
            son_actuel.stop()
            son_actuel = None
    except:
        pass

def jouer_zombies():
    global son_zombie
    try:
        if son_zombie:
            return
        # D'ABORD : si tu as mis un vrai fichier zombies_reel.mp3, on utilise celui-la
        reel = trouver_zombie_reel()
        chemin_a_jouer = reel if reel else CHEMIN_ZOMBIES
        if chemin_a_jouer and os.path.exists(chemin_a_jouer):
            son_zombie = SoundLoader.load(chemin_a_jouer)
            if son_zombie:
                son_zombie.loop = True
                son_zombie.play()
    except:
        pass

def arreter_zombies():
    global son_zombie
    try:
        if son_zombie:
            son_zombie.stop()
            son_zombie = None
    except:
        pass

EMOTIONS = [
    ("TRISTE", (1, 0.85, 0.2, 1), "triste"),
    ("EN COLERE", (1, 0.4, 0.35, 1), "colere"),
    ("STRESSE", (0.6, 0.8, 1, 1), "peur"),
    ("FATIGUE", (0.75, 0.75, 0.75, 1), "fatigue"),
    ("SEUL", (0.7, 0.6, 1, 1), "seul"),
    ("PEUR", (0.6, 0.9, 0.6, 1), "peur"),
]

class CoverImage(Image):
    def __init__(self, zoom_extra=1.0, centre_x=0.5, centre_y=0.5, **kwargs):
        self.zoom_extra = zoom_extra
        self.centre_x = centre_x
        self.centre_y = centre_y
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True
        self.size_hint = (None, None)
        self.bind(texture=self._zoom, size=self._zoom)
    def _zoom(self, *args):
        if not self.texture:
            return
        tw, th = self.texture.size
        if tw == 0 or th == 0:
            return
        if self.parent:
            pw, ph = self.parent.size
        else:
            pw, ph = Window.width, Window.height
        if pw == 0 or ph == 0:
            return
        zoom = max(pw / tw, ph / th) * self.zoom_extra
        self.size = (tw * zoom, th * zoom)
        self.center = (pw * self.centre_x, ph * self.centre_y)
    def on_parent(self, *args):
        if self.parent:
            self.parent.bind(size=self._zoom)
            Clock.schedule_once(self._zoom, 0.1)

def photo(nom, zoom_extra=1.0, centre_x=0.5, centre_y=0.5):
    cadre = FloatLayout(size_hint=(1, 1))
    for base in [DOSSIER_FACEBOOK, DOSSIER_CODE, os.getcwd()]:
        p = os.path.join(base, nom)
        if os.path.exists(p):
            img = CoverImage(source=p, zoom_extra=zoom_extra, centre_x=centre_x, centre_y=centre_y)
            cadre.add_widget(img)
            return cadre
    return Label(text="Photo introuvable :\n" + nom, color=(1,0,0,1))

def bouton(texte, couleur=(0.2,0.4,0.7,1), hauteur=110):
    return Button(text=texte, font_size=22, size_hint_y=None, height=hauteur, background_color=couleur)

def label_centre(texte, taille=13, couleur=(0,0,0,1), hauteur=20):
    lab = Label(text=texte, font_size=taille, bold=True, color=couleur, halign="center", valign="middle", size_hint_y=None, height=hauteur)
    lab.bind(size=lambda *a: setattr(lab, "text_size", (lab.width, None)))
    return lab

class VisageEmotion(Button):
    def __init__(self, taille, nom, couleur_face, type_visage, **kwargs):
        super().__init__(text="", size_hint=(None, None), size=(taille, taille+25), background_color=(0,0,0,0), background_normal="", **kwargs)
        self.taille = taille
        self.nom = nom
        self.couleur_face = couleur_face
        self.type_visage = type_visage
        self.explose = False
        self.dessiner()
        self.label_nom = Label(text=nom, font_size=15, bold=True, color=(1,1,1,1), size_hint=(None, None), size=(taille+20, 25), pos=(self.x, self.y))
        self.add_widget(self.label_nom)
        self.bind(pos=self._maj, size=self._maj)
    def dessiner(self):
        if self.explose:
            return
        self.canvas.before.clear()
        t = self.taille
        with self.canvas.before:
            Color(*self.couleur_face)
            self.visage = Ellipse(pos=(self.x, self.y+25), size=(t, t))
            Color(0, 0, 0, 0.8)
            self.contour = Line(circle=(self.center_x, self.center_y+12, t/2), width=2)
            Color(0, 0, 0, 1)
            self.oeil_g = Ellipse(pos=(self.x + t*0.28, self.y+25 + t*0.58), size=(t*0.12, t*0.12))
            self.oeil_d = Ellipse(pos=(self.x + t*0.60, self.y+25 + t*0.58), size=(t*0.12, t*0.12))
            Color(0, 0, 0, 1)
            if self.type_visage == "triste":
                self.bouche = Line(points=[self.x+t*0.30, self.y+25+t*0.30, self.x+t*0.50, self.y+25+t*0.42, self.x+t*0.70, self.y+25+t*0.30], width=2.5)
                Color(0.3, 0.6, 1, 1)
                self.larme = Ellipse(pos=(self.x+t*0.22, self.y+25+t*0.38), size=(t*0.08, t*0.14))
            elif self.type_visage == "colere":
                Color(0, 0, 0, 1)
                self.sourcil_g = Line(points=[self.x+t*0.22, self.y+25+t*0.78, self.x+t*0.42, self.y+25+t*0.68], width=3)
                self.sourcil_d = Line(points=[self.x+t*0.78, self.y+25+t*0.78, self.x+t*0.58, self.y+25+t*0.68], width=3)
                self.bouche = Line(points=[self.x+t*0.32, self.y+25+t*0.28, self.x+t*0.68, self.y+25+t*0.28], width=2.5)
            elif self.type_visage == "peur":
                Color(0, 0, 0, 1)
                self.bouche = Ellipse(pos=(self.x+t*0.40, self.y+25+t*0.20), size=(t*0.20, t*0.20))
            elif self.type_visage == "fatigue":
                Color(0, 0, 0, 1)
                self.bouche = Line(points=[self.x+t*0.35, self.y+25+t*0.28, self.x+t*0.65, self.y+25+t*0.28], width=2.5)
            else:
                Color(0, 0, 0, 1)
                self.bouche = Line(points=[self.x+t*0.30, self.y+25+t*0.30, self.x+t*0.50, self.y+25+t*0.22, self.x+t*0.70, self.y+25+t*0.30], width=2.5)
    def _maj(self, *args):
        self.dessiner()
        if hasattr(self, 'label_nom'):
            self.label_nom.pos = (self.x - 10, self.y)
            self.label_nom.size = (self.size[0]+20, 25)
    def exploser(self):
        self.explose = True
        self.canvas.before.clear()
        t = self.taille
        self.size = (t*1.4, t*1.4+25)
        cx = self.center_x
        cy = self.center_y + 12
        with self.canvas.before:
            Color(1, 0.85, 0, 1)
            Ellipse(pos=(cx - t*0.30, cy - t*0.30), size=(t*0.60, t*0.60))
            Color(1, 0.45, 0, 1)
            Ellipse(pos=(cx - t*0.18, cy - t*0.18), size=(t*0.36, t*0.36))
            Color(1, 1, 0, 1)
            for angle, dx, dy in [(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(0,0.7,0.7),(0,-0.7,0.7),(0,0.7,-0.7),(0,-0.7,-0.7)]:
                Line(points=[cx, cy, cx + dx*t*0.65, cy + dy*t*0.65], width=4)
            Color(1, 0.3, 0.3, 1)
            Ellipse(pos=(cx + t*0.55, cy + t*0.30), size=(t*0.12, t*0.12))
            Color(1, 1, 1, 1)
            Ellipse(pos=(cx - t*0.65, cy - t*0.20), size=(t*0.10, t*0.10))
            Color(1, 0.6, 0, 1)
            Ellipse(pos=(cx + t*0.20, cy - t*0.60), size=(t*0.11, t*0.11))
        self.label_nom.text = "POC !"
        self.label_nom.font_size = 20
        self.label_nom.color = (1, 1, 0, 1)

# --- FIN PARTIE 1 / 4, colle la PARTIE 2 juste en dessous ---
# EVE FINALE - PARTIE 2 / 4 - COPIE CELLE-LA JUSTE APRES LA PARTIE 1
# Bulle qui s'agrandit toute seule, rien ne sort de la case
class BulleBD(BoxLayout):
    def __init__(self, texte, **kwargs):
        total_lignes = 0
        for ligne in texte.split("\n"):
            total_lignes += max(1, (len(ligne) // 32) + 1)
        hauteur = 45 + total_lignes * 27
        if hauteur < 110:
            hauteur = 110
        if hauteur > 330:
            hauteur = 330
        super().__init__(orientation="vertical", size_hint_y=None, height=hauteur, padding=(18, 10), **kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 0.97)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[25, 25, 25, 5])
        self.bind(pos=self._maj, size=self._maj)
        lab = Label(text=texte, color=(0, 0, 0, 1), font_size=19, bold=True, halign="center", valign="middle")
        lab.bind(size=lambda *a: setattr(lab, "text_size", (lab.width - 20, None)))
        self.add_widget(lab)
        self.add_widget(Label(text="▼", color=(1,1,1,1), font_size=16, size_hint_y=None, height=16))
    def _maj(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

def bulle_eve(texte):
    return BulleBD("Eve : " + texte)

class PetiteBulle(BoxLayout):
    def __init__(self, texte, hauteur=48, taille_texte=18, **kwargs):
        super().__init__(orientation="vertical", size_hint=(1, None), height=hauteur, padding=(12, 6), **kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 0.97)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20, 20, 20, 5])
        self.bind(pos=self._maj, size=self._maj)
        self.lab = Label(text=texte, color=(0, 0, 0, 1), font_size=taille_texte, bold=True, halign="center", valign="middle")
        self.lab.bind(size=lambda *a: setattr(self.lab, "text_size", (self.lab.width - 10, None)))
        self.add_widget(self.lab)
    def _maj(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    def changer_texte(self, nouveau):
        self.lab.text = nouveau

class BulleRondeConseil(FloatLayout):
    def __init__(self, texte, **kwargs):
        super().__init__(size_hint=(None, None), size=(250, 250), pos_hint={"center_x": 0.76, "center_y": 0.74}, **kwargs)
        with self.canvas.before:
            Color(1, 0.95, 0.7, 1)
            self.cercle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self._maj, size=self._maj)
        lab = Label(text=texte, color=(0, 0, 0, 1), font_size=15, bold=True, halign="center", valign="middle",
                    size_hint=(None, None), size=(200, 180), pos_hint={"center_x": 0.5, "center_y": 0.48})
        lab.bind(size=lambda *a: setattr(lab, "text_size", (190, None)))
        self.add_widget(lab)
        titre = Label(text="Conseil", color=(0.6, 0.4, 0, 1), font_size=16, bold=True, size_hint=(None, None), size=(200, 30), pos_hint={"center_x": 0.5, "top": 0.92})
        self.add_widget(titre)
    def _maj(self, *args):
        self.cercle.pos = self.pos
        self.cercle.size = self.size

def reponse_eve(texte):
    t = texte.lower().strip()
    if "pourquoi" in t and ("triste" in t or "mal" in t):
        return "C'est une tres bonne question.\nParfois on est triste sans savoir pourquoi, et c'est normal.\nTu as le droit de te sentir comme ca.\nIl s'est passe quelque chose aujourd'hui ?"
    if "pourquoi" in t:
        return "Je t'ecoute, c'est important de se poser cette question.\nTu veux qu'on essaie de comprendre ensemble ?\nDis-moi ce qui t'es arrive."
    if "comment" in t and ("aller mieux" in t or "faire" in t):
        return "Pour aller mieux, on peut commencer doucement.\nPrends une grande respiration avec moi...\nTu veux qu'on essaie ? Bois un verre d'eau, repose-toi un peu.\nTu veux me dire ce qui te pese le plus ?"
    if "que faire" in t or "quoi faire" in t:
        return "Tu fais deja tres bien de m'en parler, c'est courageux.\nOn peut en parler doucement, sans se presser.\nTu veux me raconter ce qui t'arrive ? Je suis la."
    if "normal" in t or "est-ce que" in t or "est ce que" in t:
        return "Oui, c'est completement normal ce que tu ressens.\nBeaucoup de gens ressentent ca aussi, tu n'es pas bizarre.\nTu as le droit de te sentir comme ca.\nTu veux m'en dire plus ?"
    if "?" in t:
        return "Merci pour ta question, je t'ecoute vraiment.\nCe que tu ressens compte beaucoup pour moi.\nTu peux m'en dire un peu plus, pour que je comprenne mieux ?"
    if "triste" in t or "pleur" in t or "deprim" in t or "mal" in t:
        return "Oh... je suis vraiment desolee que tu te sentes comme ca.\nC'est dur d'etre triste, je comprends.\nJe suis la, tu n'es pas seul.\nTu veux me dire ce qui te rend triste ?"
    if "stress" in t or "angoiss" in t or "peur" in t or "paniqu" in t:
        return "Je comprends, ca doit faire peur de se sentir comme ca.\nTon coeur bat vite, c'est normal quand on est stresse.\nOn va respirer ensemble, doucement.\nC'est quoi qui te stresse le plus ? Je t'ecoute."
    if "fatigu" in t or "dors" in t or "sommeil" in t or "epuis" in t:
        return "Tu dois etre vraiment epuisee, ca se comprend.\nTon corps te dit qu'il a besoin de repos.\nTu as le droit de te reposer, tu n'as rien a prouver.\nTu dors mal en ce moment ?"
    if "seul" in t or "solitude" in t or "personne" in t:
        return "Je suis la, tu n'es plus seul maintenant.\nC'est normal de se sentir seul parfois, meme quand il y a du monde.\nMoi je suis la pour t'ecouter, vraiment.\nTu veux me raconter ?"
    if "colere" in t or "enerve" in t or "enerv" in t:
        return "C'est normal d'etre en colere, tu as le droit.\nTa colere veut te dire que quelque chose t'a fait mal.\nJe ne vais pas te juger, je t'ecoute.\nQu'est-ce qui t'a enerve ?"
    if "bien" in t or "content" in t or "super" in t or "heureux" in t or "ca va" in t:
        return "Oh super, je suis tellement contente pour toi !\nCa me fait chaud au coeur de te voir comme ca.\nRaconte-moi, c'est quoi qui te rend heureuse ?"
    if "bonjour" in t or "salut" in t or "coucou" in t:
        return "Bonjour ! Ca me fait tellement plaisir de te voir.\nComment tu te sens aujourd'hui, vraiment ?\nJe suis la pour t'ecouter."
    if "merci" in t:
        return "De rien, c'est normal, c'est pour ca que je suis la.\nTu comptes beaucoup, tu sais.\nTu veux continuer a me parler ?"
    if "au revoir" in t or "bye" in t:
        return "Tu pars deja ? Je vais etre triste...\nMais je comprends. Reviens quand tu veux, je serai la.\nPrends soin de toi."
    if "aide" in t or "aider" in t:
        return "Oui, je vais t'aider, tu n'es pas seul.\nOn va y aller doucement, ensemble.\nDis-moi, c'est quoi le plus dur pour toi en ce moment ?"
    return "Merci de me confier ca, ca me touche beaucoup.\nJe t'ecoute vraiment, prends ton temps.\nTu peux m'en dire un peu plus ? Je suis la pour toi."

class E1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="vertical")
        box.add_widget(photo(PHOTO_FACADE))
        b = bouton("Entrer voir Eve")
        b.bind(on_press=lambda x: setattr(self.manager, "current", "accueil"))
        box.add_widget(b)
        self.add_widget(box)
    def on_enter(self):
        jouer_zombies()
    def on_leave(self):
        arreter_zombies()

class E2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="vertical")
        box.add_widget(photo(PHOTO_ACCUEIL))
        box.add_widget(bulle_eve("Bienvenue, entre... Je suis Eve, je suis la pour t'ecouter."))
        b = bouton("Merci")
        b.bind(on_press=lambda x: setattr(self.manager, "current", "installation"))
        box.add_widget(b)
        self.add_widget(box)
    def on_enter(self):
        arreter_zombies()

class E3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="vertical")
        box.add_widget(photo(PHOTO_FAUTEUIL))
        box.add_widget(bulle_eve("Installe-toi dans le fauteuil, mets-toi a l'aise."))
        b = bouton("Je m'installe")
        b.bind(on_press=lambda x: setattr(self.manager, "current", "chat"))
        box.add_widget(b)
        self.add_widget(box)
    def on_enter(self):
        arreter_zombies()

class EChat(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.derniere_reponse = "Comment tu te sens aujourd'hui, vraiment ?\nEcris-moi, je t'ecoute."
        self.layout = FloatLayout()
        self.add_widget(self.layout)
    def on_enter(self):
        arreter_zombies()
        self.afficher()
    def afficher(self, reponse=None):
        if reponse:
            self.derniere_reponse = reponse
        self.layout.clear_widgets()
        self.layout.add_widget(photo(PHOTO_DISCUSSION))
        box = BoxLayout(orientation="vertical", size_hint=(1, 1), padding=10, spacing=8)
        box.add_widget(Widget(size_hint_y=1))
        box.add_widget(bulle_eve(self.derniere_reponse))
        ligne = BoxLayout(orientation="horizontal", size_hint_y=None, height=95, spacing=5)
        self.saisie = TextInput(hint_text="Ecris ici... ex: pourquoi je suis triste ?", font_size=22, multiline=False)
        ligne.add_widget(self.saisie)
        envoyer = Button(text="Envoyer", font_size=22, size_hint_x=None, width=130, background_color=(0.2,0.4,0.7,1))
        envoyer.bind(on_press=lambda x: self.envoyer_texte())
        ligne.add_widget(envoyer)
        box.add_widget(ligne)
        jeux = BoxLayout(orientation="horizontal", size_hint_y=None, height=55, spacing=5)
        jeu1 = Button(text="BOOM", font_size=17, background_color=(0.6,0.4,0.9,1))
        jeu1.bind(on_press=lambda x: setattr(self.manager, "current", "jeu"))
        jeux.add_widget(jeu1)
        jeu2 = Button(text="Respirer", font_size=17, background_color=(0.2,0.7,0.7,1))
        jeu2.bind(on_press=lambda x: setattr(self.manager, "current", "respiration"))
        jeux.add_widget(jeu2)
        box.add_widget(jeux)
        bas = BoxLayout(orientation="horizontal", size_hint_y=None, height=55, spacing=5)
        r = Button(text="Voir le recap", font_size=18, background_color=(0.4,0.7,0.4,1))
        r.bind(on_press=lambda x: setattr(self.manager, "current", "recap"))
        bas.add_widget(r)
        q = Button(text="Quitter", font_size=18, background_color=(0.8,0.3,0.3,1))
        q.bind(on_press=lambda x: setattr(self.manager, "current", "quitter"))
        bas.add_widget(q)
        box.add_widget(bas)
        self.layout.add_widget(box)
    def envoyer_texte(self):
        txt = self.saisie.text.strip()
        if txt == "":
            return
        messages.append(txt)
        rep = reponse_eve(txt)
        self.saisie.text = ""
        self.afficher(rep)

# --- FIN PARTIE 2 / 4, colle la PARTIE 3 juste en dessous ---
# EVE FINALE - PARTIE 3 / 4 - COPIE CELLE-LA JUSTE APRES LA PARTIE 2
class EJeu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.temps = 30
        self.visages = []
        self.layout = FloatLayout()
        self.add_widget(self.layout)
    def on_enter(self):
        arreter_zombies()
        self.score = 0
        self.temps = 30
        self.visages = []
        self.afficher()
        Clock.schedule_interval(self.compte_temps, 1)
        Clock.schedule_interval(self.creer_visage, 0.7)
        Clock.schedule_interval(self.bouger_visages, 0.05)
    def on_leave(self):
        Clock.unschedule(self.compte_temps)
        Clock.unschedule(self.creer_visage)
        Clock.unschedule(self.bouger_visages)
    def compte_temps(self, dt):
        self.temps -= 1
        if self.temps <= 0:
            self.fin_jeu()
            return False
        self.maj_haut()
    def maj_haut(self):
        if hasattr(self, 'bulle_score'):
            self.bulle_score.changer_texte(f"Eve : Emotions eclatees : {self.score}   Temps : {self.temps}s")
    def afficher(self):
        self.layout.clear_widgets()
        self.layout.add_widget(photo(PHOTO_DISCUSSION))
        bas = BoxLayout(orientation="vertical", size_hint=(1, None), height=235, pos_hint={"bottom": 0}, padding=(10, 5), spacing=8)
        self.bulle_encouragement = PetiteBulle("Eve : Touche un visage pour le faire exploser !", hauteur=78, taille_texte=25)
        bas.add_widget(self.bulle_encouragement)
        self.bulle_score = PetiteBulle(f"Eve : Emotions eclatees : {self.score}   Temps : {self.temps}s", hauteur=78, taille_texte=25)
        bas.add_widget(self.bulle_score)
        ligne_arreter = BoxLayout(orientation="horizontal", size_hint_y=None, height=55, spacing=5)
        ligne_arreter.add_widget(Widget(size_hint_x=1))
        quitter = Button(text="Arreter", font_size=19, size_hint_x=None, width=160, background_color=(0.8,0.3,0.3,1))
        quitter.bind(on_press=lambda x: setattr(self.manager, "current", "chat"))
        ligne_arreter.add_widget(quitter)
        bas.add_widget(ligne_arreter)
        self.layout.add_widget(bas)
    def creer_visage(self, dt):
        if self.temps <= 0:
            return False
        taille = random.randint(70, 95)
        x = random.uniform(0.02, 0.78)
        y = random.uniform(0.05, 0.35)
        vitesse = random.uniform(0.003, 0.008)
        decalage = random.uniform(-0.002, 0.002)
        nom, couleur, type_v = random.choice(EMOTIONS)
        visage = VisageEmotion(taille=taille, nom=nom, couleur_face=couleur, type_visage=type_v, pos_hint={"x": x, "y": y})
        visage.vitesse = vitesse
        visage.decalage = decalage
        visage.pos_x = x
        visage.pos_y = y
        visage.bind(on_press=lambda btn: self.eclater(btn))
        self.visages.append(visage)
        self.layout.add_widget(visage)
    def bouger_visages(self, dt):
        for visage in list(self.visages):
            if visage.explose:
                continue
            visage.pos_y += visage.vitesse
            visage.pos_x += visage.decalage
            if visage.pos_x < 0.01 or visage.pos_x > 0.80:
                visage.decalage = -visage.decalage
            visage.pos_hint = {"x": visage.pos_x, "y": visage.pos_y}
            if visage.pos_y > 0.88:
                self.enlever(visage)
    def enlever(self, visage):
        if visage in self.visages:
            self.visages.remove(visage)
        if visage in self.layout.children:
            self.layout.remove_widget(visage)
    def eclater(self, visage):
        global total_booms
        if visage.explose:
            return
        self.score += 1
        total_booms += 1
        jouer_son(CHEMIN_BOOM)
        self.maj_haut()
        phrase = random.choice(PHRASES_ENCOURAGEMENT)
        if hasattr(self, 'bulle_encouragement'):
            self.bulle_encouragement.changer_texte(f"Eve : {phrase}")
        visage.exploser()
        Clock.schedule_once(lambda dt: self.enlever(visage), 0.45)
    def fin_jeu(self):
        Clock.unschedule(self.compte_temps)
        Clock.unschedule(self.creer_visage)
        Clock.unschedule(self.bouger_visages)
        self.layout.clear_widgets()
        self.layout.add_widget(photo(PHOTO_DISCUSSION))
        bas = BoxLayout(orientation="vertical", size_hint=(1, 1), padding=10, spacing=5)
        bas.add_widget(Widget(size_hint_y=1))
        if self.score >= 20:
            msg = f"POC ! Tu as fait exploser {self.score} emotions negatives !\nTu as fait partir beaucoup de tristesse.\nTu te sens un peu plus legere ?"
        elif self.score >= 10:
            msg = f"Super ! Tu as fait exploser {self.score} emotions negatives !\nCa fait du bien, hein ?\nTu veux rejouer ou on parle ?"
        else:
            msg = f"Tu as fait exploser {self.score} emotions negatives.\nC'est deja bien, tu as pris un moment pour toi.\nTu veux reessayer ?"
        bas.add_widget(bulle_eve(msg))
        rejouer = bouton("Rejouer : faire exploser mes emotions", (0.6,0.4,0.9,1))
        def rejouer2(x):
            self.manager.current = "chat"
            Clock.schedule_once(lambda dt: setattr(self.manager, "current", "jeu"), 0.1)
        rejouer.bind(on_press=rejouer2)
        bas.add_widget(rejouer)
        retour = bouton("Retourner parler a Eve", (0.2,0.4,0.7,1))
        retour.bind(on_press=lambda x: setattr(self.manager, "current", "chat"))
        bas.add_widget(retour)
        self.layout.add_widget(bas)

class ERespiration(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.cycle = 0
        self.taille_cercle = 120
        self.phase = "pret"
        self.temps_phase = 0
        self.centre_bulle_x = 0.78
        self.centre_bulle_y = 0.58
        self.son_joue = ""
    def on_enter(self):
        arreter_zombies()
        self.cycle = 0
        self.taille_cercle = 120
        self.phase = "pret"
        self.temps_phase = 0
        self.son_joue = ""
        self.afficher()
        Clock.schedule_interval(self.animer, 0.05)
    def on_leave(self):
        arreter_son()
        Clock.unschedule(self.animer)
    def afficher(self):
        self.layout.clear_widgets()
        self.layout.add_widget(photo(PHOTO_DISCUSSION))
        self.cercle_widget = Widget(size_hint=(None, None), size=(300, 300), pos_hint={"center_x": self.centre_bulle_x, "center_y": self.centre_bulle_y})
        with self.cercle_widget.canvas:
            Color(0.3, 0.85, 0.85, 0.85)
            self.cercle = Ellipse(pos=(0, 0), size=(120, 120))
            Color(1, 1, 1, 1)
            self.cercle_contour = Line(circle=(0, 0, 60), width=3)
        self.cercle_widget.bind(pos=self._maj_cercle, size=self._maj_cercle)
        self.layout.add_widget(self.cercle_widget)
        self.texte_centre = Label(text="Pret ?", font_size=26, bold=True, color=(1,1,1,1), size_hint=(None, None), size=(220, 60), pos_hint={"center_x": self.centre_bulle_x, "center_y": self.centre_bulle_y})
        self.layout.add_widget(self.texte_centre)
        bas = BoxLayout(orientation="vertical", size_hint=(1, None), height=310, pos_hint={"bottom": 0}, padding=(10, 5), spacing=8)
        self.bulle_encouragement = PetiteBulle("Eve : Allez, respire avec moi, tu peux le faire !", hauteur=78, taille_texte=25)
        bas.add_widget(self.bulle_encouragement)
        self.bulle_consigne = PetiteBulle("Eve : Suis le cercle : il gonfle, tu inspires. Il degonfle, tu expires.", hauteur=78, taille_texte=25)
        bas.add_widget(self.bulle_consigne)
        self.bulle_cycle = PetiteBulle(f"Eve : Respirations : {total_respirations} / 6", hauteur=78, taille_texte=25)
        bas.add_widget(self.bulle_cycle)
        ligne_boutons = BoxLayout(orientation="horizontal", size_hint_y=None, height=55, spacing=5)
        recommencer = Button(text="Recommencer", font_size=19, background_color=(0.2,0.7,0.7,1))
        recommencer.bind(on_press=lambda x: self.recommencer())
        ligne_boutons.add_widget(recommencer)
        quitter = Button(text="Arreter", font_size=19, background_color=(0.8,0.3,0.3,1))
        quitter.bind(on_press=lambda x: setattr(self.manager, "current", "chat"))
        ligne_boutons.add_widget(quitter)
        bas.add_widget(ligne_boutons)
        self.layout.add_widget(bas)
        Clock.schedule_once(lambda dt: self._maj_cercle(), 0.05)
    def _maj_cercle(self, *args):
        t = self.taille_cercle
        cx = self.cercle_widget.center_x
        cy = self.cercle_widget.center_y
        self.cercle.pos = (cx - t/2, cy - t/2)
        self.cercle.size = (t, t)
        self.cercle_contour.circle = (cx, cy, t/2)
    def recommencer(self):
        arreter_son()
        self.cycle = 0
        self.phase = "pret"
        self.temps_phase = 0
        self.son_joue = ""
        self.taille_cercle = 120
        self.bulle_cycle.changer_texte(f"Eve : Respirations : {total_respirations} / 6")
        self.bulle_consigne.changer_texte("Eve : Suis le cercle : il gonfle, tu inspires. Il degonfle, tu expires.")
        self.bulle_encouragement.changer_texte("Eve : Allez, respire avec moi, tu peux le faire !")
        self.texte_centre.text = "Pret ?"
        self._maj_cercle()
    def animer(self, dt):
        global total_respirations
        self.temps_phase += dt
        if self.phase == "pret":
            self.texte_centre.text = "Pret ?"
            self.taille_cercle = 120
            self._maj_cercle()
            if self.temps_phase > 1.5:
                self.phase = "inspire"
                self.temps_phase = 0
                self.son_joue = ""
        elif self.phase == "inspire":
            self.texte_centre.text = "INSPIRE"
            self.bulle_consigne.changer_texte("Eve : Inspire doucement par le nez...")
            if self.son_joue != "inspire":
                jouer_son(CHEMIN_INSPIRE)
                self.son_joue = "inspire"
            progres = min(self.temps_phase / 4.0, 1.0)
            self.taille_cercle = 120 + (280 - 120) * progres
            self._maj_cercle()
            if self.temps_phase >= 4.0:
                self.phase = "bloque"
                self.temps_phase = 0
        elif self.phase == "bloque":
            self.texte_centre.text = "BLOQUE"
            self.bulle_consigne.changer_texte("Eve : Garde l'air... 1... 2...")
            self.taille_cercle = 280
            self._maj_cercle()
            if self.temps_phase >= 2.0:
                self.phase = "expire"
                self.temps_phase = 0
                self.son_joue = ""
        elif self.phase == "expire":
            self.texte_centre.text = "EXPIRE"
            self.bulle_consigne.changer_texte("Eve : Expire doucement par la bouche...")
            if self.son_joue != "expire":
                jouer_son(CHEMIN_EXPIRE)
                self.son_joue = "expire"
            progres = min(self.temps_phase / 5.0, 1.0)
            self.taille_cercle = 280 - (280 - 120) * progres
            self._maj_cercle()
            if self.temps_phase >= 5.0:
                self.cycle += 1
                total_respirations += 1
                self.bulle_cycle.changer_texte(f"Eve : Respirations : {total_respirations} / 6")
                phrase = random.choice(PHRASES_ENCOURAGEMENT_RESPIRATION)
                self.bulle_encouragement.changer_texte(f"Eve : {phrase}")
                if self.cycle >= 3:
                    self.fin_respiration()
                    return False
                else:
                    self.phase = "inspire"
                    self.temps_phase = 0
                    self.son_joue = ""
    def fin_respiration(self):
        arreter_son()
        Clock.unschedule(self.animer)
        self.layout.clear_widgets()
        self.layout.add_widget(photo(PHOTO_DISCUSSION))
        bas = BoxLayout(orientation="vertical", size_hint=(1, 1), padding=10, spacing=5)
        bas.add_widget(Widget(size_hint_y=1))
        bas.add_widget(bulle_eve("Bravo ! Tu as fait 3 grandes respirations !\nTu te sens plus calme ?\nTon coeur bat moins vite, hein ?\nTu as tres bien respire."))
        rejouer = bouton("Respirer encore", (0.2,0.7,0.7,1))
        def rejouer2(x):
            self.manager.current = "chat"
            Clock.schedule_once(lambda dt: setattr(self.manager, "current", "respiration"), 0.1)
        rejouer.bind(on_press=rejouer2)
        bas.add_widget(rejouer)
        retour = bouton("Retourner parler a Eve", (0.2,0.4,0.7,1))
        retour.bind(on_press=lambda x: setattr(self.manager, "current", "chat"))
        bas.add_widget(retour)
        self.layout.add_widget(bas)

# --- FIN PARTIE 3 / 4, colle la PARTIE 4 juste en dessous ---
# EVE FINALE - PARTIE 4 / 4 - COPIE CELLE-LA JUSTE APRES LA PARTIE 3
class EQuizz(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.index = 0
        self.score = 0
        self.attente = False
    def on_enter(self):
        arreter_zombies()
        self.index = 0
        self.score = 0
        self.attente = False
        self.afficher_question()
    def afficher_question(self):
        self.layout.clear_widgets()
        self.layout.add_widget(photo(PHOTO_DISCUSSION))
        q, options, bonne, explication = QUESTIONS_QUIZZ[self.index]
        box = BoxLayout(orientation="vertical", size_hint=(1, 1), padding=10, spacing=8)
        box.add_widget(Widget(size_hint_y=1))
        box.add_widget(bulle_eve(q))
        for i, opt in enumerate(options):
            b = bouton(opt, (0.2,0.4,0.7,1), hauteur=70)
            b.bind(on_press=lambda x, idx=i: self.repondre(idx))
            box.add_widget(b)
        box.add_widget(Widget(size_hint_y=None, height=10))
        self.bulle_encouragement = PetiteBulle(f"Eve : Question {self.index+1} / 5 - Tu peux le faire !", hauteur=78, taille_texte=25)
        box.add_widget(self.bulle_encouragement)
        self.bulle_score = PetiteBulle(f"Eve : Bonnes reponses : {self.score} / 5", hauteur=78, taille_texte=25)
        box.add_widget(self.bulle_score)
        quitter = bouton("Arreter", (0.8,0.3,0.3,1), hauteur=55)
        quitter.bind(on_press=lambda x: setattr(self.manager, "current", "chat"))
        box.add_widget(quitter)
        self.layout.add_widget(box)
    def repondre(self, idx):
        global total_quizz
        if self.attente:
            return
        self.attente = True
        q, options, bonne, explication = QUESTIONS_QUIZZ[self.index]
        if idx == bonne:
            self.score += 1
            total_quizz += 1
            phrase = random.choice(PHRASES_ENCOURAGEMENT_QUIZZ)
            self.bulle_encouragement.changer_texte(f"Eve : {phrase}")
            self.bulle_score.changer_texte(f"Eve : Bonnes reponses : {self.score} / 5")
            jouer_son(CHEMIN_BOOM)
        else:
            self.bulle_encouragement.changer_texte("Eve : Ce n'est pas grave, on apprend ensemble !")
        Clock.schedule_once(lambda dt: self.montrer_explication(explication), 1.2)
    def montrer_explication(self, explication):
        self.layout.clear_widgets()
        self.layout.add_widget(photo(PHOTO_DISCUSSION))
        box = BoxLayout(orientation="vertical", size_hint=(1, 1), padding=10, spacing=8)
        box.add_widget(Widget(size_hint_y=1))
        box.add_widget(bulle_eve(explication))
        suivant = bouton("Question suivante", (0.4,0.7,0.4,1))
        suivant.bind(on_press=lambda x: self.suivante())
        box.add_widget(suivant)
        self.layout.add_widget(box)
    def suivante(self):
        self.attente = False
        self.index += 1
        if self.index >= len(QUESTIONS_QUIZZ):
            self.fin_quizz()
        else:
            self.afficher_question()
    def fin_quizz(self):
        self.layout.clear_widgets()
        self.layout.add_widget(photo(PHOTO_DISCUSSION))
        box = BoxLayout(orientation="vertical", size_hint=(1, 1), padding=10, spacing=8)
        box.add_widget(Widget(size_hint_y=1))
        if self.score == 5:
            msg = f"Bravo ! 5 / 5 ! Tu as tout compris !\nTu es trop forte, Eve est super fiere de toi !"
        elif self.score >= 3:
            msg = f"Super ! {self.score} / 5 bonnes reponses !\nTu as tres bien appris, continue !"
        else:
            msg = f"Tu as eu {self.score} / 5.\nCe n'est pas grave, on apprend ensemble.\nTu veux rejouer ?"
        box.add_widget(bulle_eve(msg))
        rejouer = bouton("Rejouer au Quizz Surprise", (1,0.7,0.2,1))
        def rejouer2(x):
            self.manager.current = "chat"
            Clock.schedule_once(lambda dt: setattr(self.manager, "current", "quizz"), 0.1)
        rejouer.bind(on_press=rejouer2)
        box.add_widget(rejouer)
        retour = bouton("Retourner parler a Eve", (0.2,0.4,0.7,1))
        retour.bind(on_press=lambda x: setattr(self.manager, "current", "chat"))
        box.add_widget(retour)
        self.layout.add_widget(box)

class ERecap(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
    def on_enter(self):
        arreter_zombies()
        self.layout.clear_widgets()
        self.layout.add_widget(photo(PHOTO_CARNET, zoom_extra=0.80, centre_x=0.50, centre_y=0.50))
        conseil_texte = "Prends ton temps,\nrepose-toi.\n\nJe ne suis pas\nun vrai medecin.\nParles-en a un\nvrai psychologue\nsi ca continue."
        self.layout.add_widget(BulleRondeConseil(conseil_texte))
        if messages:
            resume = "Tu m'as dit : " + ", ".join(messages[-3:])
        else:
            resume = "Tu n'as pas encore parle avec Eve."
        a_parle = len(messages) >= 1
        a_booms = total_booms >= 18
        a_respire = total_respirations >= 6
        texte_recap = "Voila ce que j'ai retenu : " + resume + "\n\n"
        texte_recap += f"Parler : {len(messages)} / 1\n"
        texte_recap += f"POC : {total_booms} / 18 emotions !\n"
        texte_recap += f"Respiration : {total_respirations} / 6 fois !\n"
        texte_recap += f"Quizz Surprise : {total_quizz} bonnes reponses !"
        if a_parle and a_booms and a_respire:
            texte_recap += "\nBravo, tu as tout fait pour ton diplome !"
        bas = BoxLayout(orientation="vertical", size_hint=(1, 1), padding=10, spacing=5)
        bas.add_widget(Widget(size_hint_y=1))
        bas.add_widget(bulle_eve(texte_recap))
        if a_parle and a_booms and a_respire:
            diplome_btn = bouton("Voir mon Diplome de Courage !", (1, 0.85, 0.2, 1))
            diplome_btn.bind(on_press=lambda x: setattr(self.manager, "current", "diplome"))
            bas.add_widget(diplome_btn)
        else:
            manque = []
            if not a_parle:
                manque.append("parle 1 fois avec Eve")
            if not a_booms:
                manque.append(f"eclate encore {18 - total_booms} emotions")
            if not a_respire:
                manque.append(f"respire encore {6 - total_respirations} fois")
            info = Label(text="Pour avoir ton diplome : " + " + ".join(manque), font_size=16, bold=True, color=(1,1,1,1), size_hint_y=None, height=30)
            bas.add_widget(info)
        b = bouton("Retourner parler")
        b.bind(on_press=lambda x: setattr(self.manager, "current", "chat"))
        bas.add_widget(b)
        q = bouton("Quitter", (0.8,0.3,0.3,1))
        q.bind(on_press=lambda x: setattr(self.manager, "current", "quitter"))
        bas.add_widget(q)
        self.layout.add_widget(bas)

class EDiplome(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
    def on_enter(self):
        arreter_zombies()
        jouer_son(CHEMIN_INSPIRE)
        self.layout.clear_widgets()
        self.layout.add_widget(photo(PHOTO_CARNET, zoom_extra=0.80, centre_x=0.50, centre_y=0.50))
        voile = Widget(size_hint=(1, 1))
        with voile.canvas:
            Color(0, 0, 0, 0.10)
            self.rect_voile = RoundedRectangle(pos=(0, 0), size=Window.size)
        voile.bind(size=lambda *a: setattr(self.rect_voile, "size", voile.size))
        self.layout.add_widget(voile)
        self.cadre_diplome = BoxLayout(orientation="vertical", size_hint=(0.38, 0.38), pos_hint={"right": 0.98, "top": 0.80}, padding=6, spacing=1)
        with self.cadre_diplome.canvas.before:
            Color(1, 0.98, 0.85, 1)
            self.fond_diplome = RoundedRectangle(pos=self.cadre_diplome.pos, size=self.cadre_diplome.size, radius=[10])
            Color(1, 0.75, 0.1, 1)
            self.bordure_diplome = Line(rectangle=(self.cadre_diplome.x+4, self.cadre_diplome.y+4, self.cadre_diplome.width-8, self.cadre_diplome.height-8), width=2)
        self.cadre_diplome.bind(pos=self._maj_diplome, size=self._maj_diplome)
        self.cadre_diplome.add_widget(label_centre("* * * * *", taille=18, couleur=(1, 0.75, 0.1, 1), hauteur=22))
        self.cadre_diplome.add_widget(label_centre("DIPLOME DE COURAGE", taille=17, couleur=(0.6, 0.4, 0, 1), hauteur=24))
        self.cadre_diplome.add_widget(label_centre("- - - * - - -", taille=15, couleur=(0.8, 0.4, 0.6, 1), hauteur=20))
        self.cadre_diplome.add_widget(label_centre("Decerne a toi !", taille=15, couleur=(0, 0, 0, 1), hauteur=20))
        self.cadre_diplome.add_widget(label_centre("<3  +  <3", taille=16, couleur=(0.9, 0.2, 0.4, 1), hauteur=20))
        texte_milieu = Label(text=f"{total_booms} emotions explosees !\n{total_respirations} respirations !\nTu as parle avec Eve !", font_size=15, bold=True, color=(0, 0, 0, 1), halign="center", valign="middle", size_hint_y=None, height=52)
        texte_milieu.bind(size=lambda *a: setattr(texte_milieu, "text_size", (texte_milieu.width, None)))
        self.cadre_diplome.add_widget(texte_milieu)
        self.cadre_diplome.add_widget(label_centre("+ + + + +", taille=16, couleur=(1, 0.6, 0.2, 1), hauteur=20))
        self.cadre_diplome.add_widget(label_centre("Signe : Eve", taille=14, couleur=(0.2, 0.4, 0.7, 1), hauteur=19))
        self.cadre_diplome.add_widget(label_centre("Tres fiere de toi !", taille=15, couleur=(0.8, 0.2, 0.2, 1), hauteur=20))
        self.cadre_diplome.add_widget(label_centre("<3  +  <3", taille=16, couleur=(0.9, 0.2, 0.4, 1), hauteur=20))
        self.cadre_diplome.add_widget(label_centre("* * * * *", taille=18, couleur=(1, 0.75, 0.1, 1), hauteur=22))
        self.layout.add_widget(self.cadre_diplome)
        Clock.schedule_once(lambda dt: self._maj_diplome(), 0.05)
        bas = BoxLayout(orientation="vertical", size_hint=(1, None), height=130, pos_hint={"bottom": 0}, padding=10, spacing=5)
        retour = bouton("Retour au recap", (0.2,0.4,0.7,1), hauteur=55)
        retour.bind(on_press=lambda x: setattr(self.manager, "current", "recap"))
        bas.add_widget(retour)
        chat = bouton("Retourner parler a Eve", (0.4,0.7,0.4,1), hauteur=55)
        chat.bind(on_press=lambda x: setattr(self.manager, "current", "chat"))
        bas.add_widget(chat)
        self.layout.add_widget(bas)
    def _maj_diplome(self, *args):
        if hasattr(self, 'fond_diplome'):
            self.fond_diplome.pos = self.cadre_diplome.pos
            self.fond_diplome.size = self.cadre_diplome.size
        if hasattr(self, 'bordure_diplome'):
            self.bordure_diplome.rectangle = (self.cadre_diplome.x+4, self.cadre_diplome.y+4, self.cadre_diplome.width-8, self.cadre_diplome.height-8)

class EQuitter(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="vertical")
        box.add_widget(photo(PHOTO_PORTE))
        box.add_widget(bulle_eve("Oh, tu veux deja partir ? T'es sur ? Tu veux pas qu'on fasse un petit quizz surprise ?"))
        quizz_btn = bouton("Oui, on fait un petit quizz surprise !", (1,0.7,0.2,1))
        quizz_btn.bind(on_press=lambda x: setattr(self.manager, "current", "quizz"))
        box.add_widget(quizz_btn)
        r = bouton("Non, je reste", (0.4,0.7,0.4,1))
        r.bind(on_press=lambda x: setattr(self.manager, "current", "chat"))
        box.add_widget(r)
        p = bouton("Oui, je quitte", (0.8,0.3,0.3,1))
        p.bind(on_press=lambda x: self.partir())
        box.add_widget(p)
        self.add_widget(box)
    def on_enter(self):
        arreter_zombies()
    def partir(self):
        global total_booms, total_respirations, total_quizz
        messages.clear()
        total_booms = 0
        total_respirations = 0
        total_quizz = 0
        self.manager.current = "facade"

class EveApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(E1(name="facade"))
        sm.add_widget(E2(name="accueil"))
        sm.add_widget(E3(name="installation"))
        sm.add_widget(EChat(name="chat"))
        sm.add_widget(EJeu(name="jeu"))
        sm.add_widget(ERespiration(name="respiration"))
        sm.add_widget(EQuizz(name="quizz"))
        sm.add_widget(ERecap(name="recap"))
        sm.add_widget(EDiplome(name="diplome"))
        sm.add_widget(EQuitter(name="quitter"))
        return sm

EveApp().run()