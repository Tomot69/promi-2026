// Promi+Design.swift — LE JEU DE COULEURS ET DE POLICES DE PROMI.
//
// Engendré depuis PROMI-TOKENS.json le 2026-09-20. Ne pas modifier à la main :
// régénérer (scratchpad/gen_swift.py). Aucune vue n'écrit une couleur ni une police :
// elles passent toutes par ce fichier, comme dans le prototype HTML.
//
// POLICES
//   titre    PromiLate-Regular.otf (Polices Promi/)
//            Police propre à Promi.
//   libelle  Gilbert-Bold.woff2
//            CC BY-SA 4.0 — Ogilvy & Mather / Type With Pride. Crédit obligatoire, glyphes non modifiables.
//   texte    Atkinson-{Regular,Medium,Bold}.woff2
//            SIL Open Font License 1.1 — Braille Institute of America.
//   marque   PromiLate-Regular.otf (Polices Promi/)
//            Police propre à Promi.

import SwiftUI

// MARK: - Les rôles. Ils basculent avec le mode ; c'est ce qu'une vue emploie.
extension Color {
    enum Promi {
        /// clair #F7F0DE · sombre #100D0B
        static func fond(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.0627, green: 0.0510, blue: 0.0431) : Color(red: 0.9686, green: 0.9412, blue: 0.8706)
        }
        /// clair #201908 · sombre #F7F0DE
        static func encre(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.9686, green: 0.9412, blue: 0.8706) : Color(red: 0.1255, green: 0.0980, blue: 0.0314)
        }
        /// clair #F7EBD6 · sombre #211B05
        static func surface(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.1294, green: 0.1059, blue: 0.0196) : Color(red: 0.9686, green: 0.9216, blue: 0.8392)
        }
        /// clair #FAF4E8 · sombre #251F11
        static func surfaceHaute(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.1451, green: 0.1216, blue: 0.0667) : Color(red: 0.9804, green: 0.9569, blue: 0.9098)
        }
        /// clair #6E6350 · sombre #928166
        static func sousTexte(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.5725, green: 0.5059, blue: 0.4000) : Color(red: 0.4314, green: 0.3882, blue: 0.3137)
        }
        /// clair #C8BAA4 · sombre #493D28
        static func grip(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.2863, green: 0.2392, blue: 0.1569) : Color(red: 0.7843, green: 0.7294, blue: 0.6431)
        }
        /// #2B1020
        static let exception = Color(red: 0.1686, green: 0.0627, blue: 0.1255)
        /// #0B4A2A
        static let crete = Color(red: 0.0431, green: 0.2902, blue: 0.1647)
        /// #43291C
        static let brunEncre = Color(red: 0.2627, green: 0.1608, blue: 0.1098)
        /// #82AEF8
        static let promi = Color(red: 0.5098, green: 0.6824, blue: 0.9725)
        /// #FFB8D2
        static let chiche = Color(red: 1.0000, green: 0.7216, blue: 0.8235)
        /// #C9A8F5
        static let nuee = Color(red: 0.7882, green: 0.6588, blue: 0.9608)
        /// #AE3929
        static let gardeDeCote = Color(red: 0.6824, green: 0.2235, blue: 0.1608)
        /// #00341A
        static let tenu = Color(red: 0.0000, green: 0.2039, blue: 0.1020)
        /// #00341A
        static let tenuClair = Color(red: 0.0000, green: 0.2039, blue: 0.1020)
        /// #8FE08F
        static let amande = Color(red: 0.5608, green: 0.8784, blue: 0.5608)
        /// #DD4D23
        static let aTenir = Color(red: 0.8667, green: 0.3020, blue: 0.1373)
        /// #291547
        static let enCours = Color(red: 0.1608, green: 0.0824, blue: 0.2784)
        /// #291547
        static let enCoursClair = Color(red: 0.1608, green: 0.0824, blue: 0.2784)
        /// #00341A
        static let encreSurTenu = Color(red: 0.0000, green: 0.2039, blue: 0.1020)
        /// #C4A2F5
        static let promiClair = Color(red: 0.7686, green: 0.6353, blue: 0.9608)
        /// #F5AC9E
        static let chicheClair = Color(red: 0.9608, green: 0.6745, blue: 0.6196)
        /// #E6D8FA
        static let nueeClair = Color(red: 0.9020, green: 0.8471, blue: 0.9804)
        /// #E6D8FA
        static let lilas = Color(red: 0.9020, green: 0.8471, blue: 0.9804)
        /// #C9A8F5
        static let mauveClair = Color(red: 0.7882, green: 0.6588, blue: 0.9608)
        /// clair #CFE5FE · sombre #0E78F2 (DÉFINITIF — Tom, 6 oct. 2026, v134 : choisi sur son iPhone)
        static func corpsPromi(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.0549, green: 0.4706, blue: 0.9490) : Color(red: 0.8118, green: 0.8980, blue: 0.9961)
        }
        /// clair #FFF4FC · sombre #7C3F58
        static func corpsChiche(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.4863, green: 0.2471, blue: 0.3451) : Color(red: 1.0000, green: 0.9569, blue: 0.9882)
        }
        /// clair #EEE4F8 · sombre #5D4978
        static func corpsNuee(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.3647, green: 0.2863, blue: 0.4706) : Color(red: 0.9333, green: 0.8941, blue: 0.9725)
        }
        /// #2B1020
        static let corpsTenu = Color(red: 0.1686, green: 0.0627, blue: 0.1255)
        /// clair #EFC3B9 · sombre #533336
        static func corpsATenir(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.3255, green: 0.2000, blue: 0.2118) : Color(red: 0.9373, green: 0.7647, blue: 0.7255)
        }
        /// clair #EFC3B9 · sombre #4B2D30
        static func corpsGarde(_ s: ColorScheme) -> Color {
            s == .dark ? Color(red: 0.2941, green: 0.1765, blue: 0.1882) : Color(red: 0.9373, green: 0.7647, blue: 0.7255)
        }
        /// #FFFFFF
        static let blanc = Color(red: 1.0000, green: 1.0000, blue: 1.0000)
        /// #000000
        static let noir = Color(red: 0.0000, green: 0.0000, blue: 0.0000)
    }
}

// MARK: - Les niveaux de texte. Un texte de l'app est toujours l'un des sept.
extension Font {
    enum Promi {
        /// 36 pt · graisse 600
        static let titre = Font.custom("Fraunces", size: 36)
        /// 22 pt · graisse 700 · CAPITALES
        static let sousTitre = Font.custom("Gilbert-Bold", size: 22)
        /// 16 pt · graisse 400
        static let texte = Font.custom("AtkinsonHyperlegibleNext", size: 16)
        /// 16 pt · graisse 700
        static let accent = Font.custom("AtkinsonHyperlegibleNext", size: 16)
        /// 14 pt · graisse 400
        static let petit = Font.custom("AtkinsonHyperlegibleNext", size: 14)
        /// 13 pt · graisse 400 · opacité 0.65
        static let meta = Font.custom("AtkinsonHyperlegibleNext", size: 13)
        /// 15 pt · graisse 700 · CAPITALES
        static let libelle = Font.custom("Gilbert-Bold", size: 15)
        /// PromiLate — titres d'écran, mot-marque, phrases d'action du trait. Une seule graisse.
        static func marque(_ taille: CGFloat) -> Font { Font.custom("PromiLate-Regular", size: taille) }
    }
}

// MARK: - Le style complet d'un niveau : la police, les capitales, l'opacité.
struct NiveauPromi: ViewModifier {
    let police: Font
    let capitales: Bool
    let opacite: Double
    func body(content: Content) -> some View {
        content.font(police)
            .textCase(capitales ? .uppercase : nil)
            .opacity(opacite)
    }
}

extension View {
    func promiTitre() -> some View {
        modifier(NiveauPromi(police: .Promi.titre, capitales: false, opacite: 1.0))
    }
    func promiSousTitre() -> some View {
        modifier(NiveauPromi(police: .Promi.sousTitre, capitales: true, opacite: 1.0))
    }
    func promiTexte() -> some View {
        modifier(NiveauPromi(police: .Promi.texte, capitales: false, opacite: 1.0))
    }
    func promiAccent() -> some View {
        modifier(NiveauPromi(police: .Promi.accent, capitales: false, opacite: 1.0))
    }
    func promiPetit() -> some View {
        modifier(NiveauPromi(police: .Promi.petit, capitales: false, opacite: 1.0))
    }
    func promiMeta() -> some View {
        modifier(NiveauPromi(police: .Promi.meta, capitales: false, opacite: 0.65))
    }
    func promiLibelle() -> some View {
        modifier(NiveauPromi(police: .Promi.libelle, capitales: true, opacite: 1.0))
    }
}

// MARK: - La palette FIXE. Une valeur par couleur, elle ne bascule jamais.
// Une vue n'y touche pas : elle sert aux rôles ci-dessus et au report d'écrans
// que le prototype peint encore avec une nuance sans rôle nommé.
extension Color {
    enum PalettePromi {
        static let beige26 = Color(red: 0.2706, green: 0.2353, blue: 0.1961)   // #453C32
        static let beige262 = Color(red: 0.2863, green: 0.2392, blue: 0.1569)   // #493D28
        static let beige27 = Color(red: 0.2941, green: 0.2471, blue: 0.1608)   // #4B3F29
        static let beige30 = Color(red: 0.2941, green: 0.2745, blue: 0.2353)   // #4B463C
        static let beige302 = Color(red: 0.2941, green: 0.2784, blue: 0.2510)   // #4B4740
        static let beige37 = Color(red: 0.3804, green: 0.3412, blue: 0.2510)   // #615740
        static let beige38 = Color(red: 0.3882, green: 0.3412, blue: 0.2549)   // #635741
        static let beige40 = Color(red: 0.3961, green: 0.3686, blue: 0.3333)   // #655E55
        static let beige42 = Color(red: 0.4235, green: 0.3804, blue: 0.3412)   // #6C6157
        static let beige422 = Color(red: 0.4235, green: 0.3843, blue: 0.3255)   // #6C6253
        static let beige43 = Color(red: 0.4235, green: 0.3961, blue: 0.3451)   // #6C6558
        static let beige44 = Color(red: 0.4314, green: 0.3882, blue: 0.3137)   // #6E6350
        static let beige45 = Color(red: 0.4392, green: 0.4196, blue: 0.3922)   // #706B64
        static let beige452 = Color(red: 0.4353, green: 0.4157, blue: 0.3529)   // #6F6A5A
        static let beige47 = Color(red: 0.4667, green: 0.4314, blue: 0.3922)   // #776E64
        static let beige53 = Color(red: 0.5451, green: 0.4902, blue: 0.4353)   // #8B7D6F
        static let beige55 = Color(red: 0.5725, green: 0.5059, blue: 0.4000)   // #928166
        static let beige56 = Color(red: 0.6353, green: 0.5804, blue: 0.4863)   // #A2947C
        static let beige58 = Color(red: 0.5569, green: 0.5373, blue: 0.4941)   // #8E897E
        static let beige582 = Color(red: 0.5804, green: 0.5412, blue: 0.4471)   // #948A72
        static let beige59 = Color(red: 0.5765, green: 0.5490, blue: 0.5059)   // #938C81
        static let beige592 = Color(red: 0.5922, green: 0.5490, blue: 0.5098)   // #978C82
        static let beige60 = Color(red: 0.6157, green: 0.5529, blue: 0.4627)   // #9D8D76
        static let beige61 = Color(red: 0.6078, green: 0.5647, blue: 0.5020)   // #9B9080
        static let beige62 = Color(red: 0.6039, green: 0.5686, blue: 0.5216)   // #9A9185
        static let beige65 = Color(red: 0.6588, green: 0.6000, blue: 0.5216)   // #A89985
        static let beige652 = Color(red: 0.6588, green: 0.6000, blue: 0.5294)   // #A89987
        static let beige67 = Color(red: 0.6588, green: 0.6275, blue: 0.5569)   // #A8A08E
        static let beige69 = Color(red: 0.6863, green: 0.6431, blue: 0.5961)   // #AFA498
        static let blanc100 = Color(red: 1.0000, green: 1.0000, blue: 1.0000)   // #FFFFFF
        static let bleu08 = Color(red: 0.0078, green: 0.1294, blue: 0.2510)   // #022140
        static let bleu13 = Color(red: 0.0745, green: 0.2000, blue: 0.3216)   // #133352
        static let bleu14 = Color(red: 0.0157, green: 0.2157, blue: 0.3647)   // #04375D
        static let bleu142 = Color(red: 0.0196, green: 0.2078, blue: 0.3647)   // #05355D
        static let bleu17 = Color(red: 0.1451, green: 0.2510, blue: 0.3647)   // #25405D
        static let bleu172 = Color(red: 0.1608, green: 0.2588, blue: 0.3804)   // #294261
        static let bleu18 = Color(red: 0.1725, green: 0.2745, blue: 0.3961)   // #2C4665
        static let bleu19 = Color(red: 0.1216, green: 0.2784, blue: 0.4392)   // #1F4770
        static let bleu192 = Color(red: 0.1608, green: 0.2784, blue: 0.4039)   // #294767
        static let bleu193 = Color(red: 0.1686, green: 0.2784, blue: 0.4039)   // #2B4767
        static let bleu194 = Color(red: 0.1765, green: 0.2784, blue: 0.3961)   // #2D4765
        static let bleu195 = Color(red: 0.1569, green: 0.2902, blue: 0.4431)   // #284A71
        static let bleu20 = Color(red: 0.1137, green: 0.2941, blue: 0.4706)   // #1D4B78
        static let bleu22 = Color(red: 0.2196, green: 0.3294, blue: 0.4588)   // #385475
        static let bleu35 = Color(red: 0.2000, green: 0.3255, blue: 0.5098)   // #335382
        static let cobalt50 = Color(red: 0.0549, green: 0.4706, blue: 0.9490)   // #0E78F2 (définitif, v134)
        static let bleu45 = Color(red: 0.5098, green: 0.6824, blue: 0.9725)   // #82AEF8
        static let bleu45Txt = Color(red: 0.5098, green: 0.6824, blue: 0.9725)   // #82AEF8
        static let bleu46 = Color(red: 0.5098, green: 0.6863, blue: 0.9804)   // #82AFFA
        static let bleu50 = Color(red: 0.5451, green: 0.7098, blue: 0.9569)   // #8BB5F4
        static let bleu51 = Color(red: 0.5686, green: 0.7176, blue: 0.9098)   // #91B7E8
        static let bleu512 = Color(red: 0.5333, green: 0.7176, blue: 0.9765)   // #88B7F9
        static let bleu54 = Color(red: 0.5608, green: 0.7333, blue: 0.9686)   // #8FBBF7
        static let bleu60 = Color(red: 0.5725, green: 0.7569, blue: 0.9961)   // #92C1FE
        static let bleu62 = Color(red: 0.5961, green: 0.7647, blue: 0.9922)   // #98C3FD
        static let bleu622 = Color(red: 0.6549, green: 0.7608, blue: 0.9647)   // #A7C2F6
        static let bleu67 = Color(red: 0.6118, green: 0.7961, blue: 0.9961)   // #9CCBFE
        static let bleu80 = Color(red: 0.7255, green: 0.8549, blue: 1.0000)   // #B9DAFF
        static let bleu83 = Color(red: 0.7529, green: 0.8667, blue: 0.9961)   // #C0DDFE
        static let bleu85 = Color(red: 0.8039, green: 0.8627, blue: 1.0000)   // #CDDCFF
        static let brun03 = Color(red: 0.0627, green: 0.0510, blue: 0.0431)   // #100D0B
        static let brun05 = Color(red: 0.0902, green: 0.0627, blue: 0.0000)   // #171000
        static let brun052 = Color(red: 0.0706, green: 0.0549, blue: 0.0196)   // #120E05
        static let brun06 = Color(red: 0.0824, green: 0.0745, blue: 0.0588)   // #15130F
        static let brun062 = Color(red: 0.1020, green: 0.0706, blue: 0.0039)   // #1A1201
        static let brun063 = Color(red: 0.0902, green: 0.0706, blue: 0.0000)   // #171200
        static let brun064 = Color(red: 0.1020, green: 0.0667, blue: 0.0000)   // #1A1100
        static let brun07 = Color(red: 0.1176, green: 0.0745, blue: 0.0039)   // #1E1301
        static let brun08 = Color(red: 0.1020, green: 0.0863, blue: 0.0745)   // #1A1613
        static let brun082 = Color(red: 0.1137, green: 0.0863, blue: 0.0000)   // #1D1600
        static let brun083 = Color(red: 0.1137, green: 0.0902, blue: 0.0000)   // #1D1700
        static let brun084 = Color(red: 0.1216, green: 0.0863, blue: 0.0196)   // #1F1605
        static let brun09 = Color(red: 0.1255, green: 0.0980, blue: 0.0314)   // #201908
        static let brun092 = Color(red: 0.1137, green: 0.1020, blue: 0.0902)   // #1D1A17
        static let brun10 = Color(red: 0.1294, green: 0.1059, blue: 0.0196)   // #211B05
        static let brun11 = Color(red: 0.1373, green: 0.1176, blue: 0.0078)   // #231E02
        static let brun12 = Color(red: 0.1412, green: 0.1255, blue: 0.0235)   // #242006
        static let brun122 = Color(red: 0.1451, green: 0.1216, blue: 0.0667)   // #251F11
        static let brun14 = Color(red: 0.1843, green: 0.1255, blue: 0.1098)   // #2F201C
        static let brun15 = Color(red: 0.1725, green: 0.1490, blue: 0.0941)   // #2C2618
        static let brun19 = Color(red: 0.2157, green: 0.1765, blue: 0.1176)   // #372D1E
        static let brun192 = Color(red: 0.2314, green: 0.1608, blue: 0.1412)   // #3B2924
        static let brun193 = Color(red: 0.2627, green: 0.1608, blue: 0.1098)   // #43291C
        static let brun21 = Color(red: 0.2353, green: 0.1961, blue: 0.1176)   // #3C321E
        static let creme70 = Color(red: 0.7059, green: 0.6510, blue: 0.5765)   // #B4A693
        static let creme76 = Color(red: 0.7412, green: 0.7098, blue: 0.6667)   // #BDB5AA
        static let creme762 = Color(red: 0.8314, green: 0.6941, blue: 0.4980)   // #D4B17F
        static let creme78 = Color(red: 0.7843, green: 0.7294, blue: 0.6431)   // #C8BAA4
        static let creme79 = Color(red: 0.7922, green: 0.7451, blue: 0.6431)   // #CABEA4
        static let creme792 = Color(red: 0.7961, green: 0.7373, blue: 0.6510)   // #CBBCA6
        static let creme83 = Color(red: 0.8902, green: 0.7647, blue: 0.6157)   // #E3C39D
        static let creme85 = Color(red: 0.9373, green: 0.7647, blue: 0.7255)   // #EFC3B9
        static let creme852 = Color(red: 0.9804, green: 0.7608, blue: 0.6588)   // #FAC2A8
        static let creme853 = Color(red: 0.9059, green: 0.7804, blue: 0.6235)   // #E7C79F
        static let creme87 = Color(red: 0.8784, green: 0.8157, blue: 0.6980)   // #E0D0B2
        static let creme88 = Color(red: 0.9255, green: 0.8118, blue: 0.7765)   // #ECCFC6
        static let creme90 = Color(red: 0.9137, green: 0.8471, blue: 0.7176)   // #E9D8B7
        static let creme902 = Color(red: 0.9176, green: 0.8510, blue: 0.7255)   // #EAD9B9
        static let creme903 = Color(red: 0.9373, green: 0.8431, blue: 0.7176)   // #EFD7B7
        static let creme904 = Color(red: 0.9882, green: 0.8196, blue: 0.7569)   // #FCD1C1
        static let creme91 = Color(red: 0.9294, green: 0.8588, blue: 0.7412)   // #EDDBBD
        static let creme912 = Color(red: 0.9294, green: 0.8588, blue: 0.7843)   // #EDDBC8
        static let creme92 = Color(red: 0.8941, green: 0.8431, blue: 0.7333)   // #E4D7BB
        static let creme922 = Color(red: 0.9373, green: 0.8902, blue: 0.7804)   // #EFE3C7
        static let creme923 = Color(red: 0.9451, green: 0.8588, blue: 0.8275)   // #F1DBD3
        static let creme93 = Color(red: 0.9451, green: 0.8824, blue: 0.7725)   // #F1E1C5
        static let creme932 = Color(red: 0.9294, green: 0.8745, blue: 0.8235)   // #EDDFD2
        static let creme933 = Color(red: 0.9373, green: 0.8784, blue: 0.8078)   // #EFE0CE
        static let creme934 = Color(red: 0.9294, green: 0.8824, blue: 0.8392)   // #EDE1D6
        static let creme94 = Color(red: 0.9137, green: 0.8980, blue: 0.8353)   // #E9E5D5
        static let creme95 = Color(red: 0.9686, green: 0.9412, blue: 0.8706)   // #F7F0DE
        static let creme952 = Color(red: 0.9529, green: 0.9059, blue: 0.8196)   // #F3E7D1
        static let creme953 = Color(red: 0.9569, green: 0.9059, blue: 0.8196)   // #F4E7D1
        static let creme954 = Color(red: 0.9333, green: 0.9020, blue: 0.8353)   // #EEE6D5
        static let creme955 = Color(red: 0.9608, green: 0.8980, blue: 0.7922)   // #F5E5CA
        static let creme956 = Color(red: 0.9529, green: 0.8980, blue: 0.8431)   // #F3E5D7
        static let creme957 = Color(red: 0.9490, green: 0.9059, blue: 0.8471)   // #F2E7D8
        static let creme97 = Color(red: 0.9686, green: 0.9216, blue: 0.8392)   // #F7EBD6
        static let creme99 = Color(red: 0.9804, green: 0.9569, blue: 0.9098)   // #FAF4E8
        static let crete27 = Color(red: 0.0431, green: 0.2902, blue: 0.1647)   // #0B4A2A
        static let framboise08 = Color(red: 0.1255, green: 0.0706, blue: 0.1294)   // #201221
        static let framboise082 = Color(red: 0.1490, green: 0.0588, blue: 0.1216)   // #260F1F
        static let framboise10 = Color(red: 0.2196, green: 0.0510, blue: 0.1451)   // #380D25
        static let framboise11 = Color(red: 0.2392, green: 0.0588, blue: 0.1373)   // #3D0F23
        static let framboise35 = Color(red: 0.4863, green: 0.2471, blue: 0.3451)   // #7C3F58
        static let framboise54 = Color(red: 1.0000, green: 0.7216, blue: 0.8235)   // #FFB8D2
        static let framboise54Txt = Color(red: 1.0000, green: 0.7216, blue: 0.8235)   // #FFB8D2
        static let framboise70 = Color(red: 0.9843, green: 0.8078, blue: 1.0000)   // #FBCEFF
        static let framboise91 = Color(red: 1.0000, green: 0.9373, blue: 0.9804)   // #FFEFFA
        static let framboise94 = Color(red: 1.0000, green: 0.9569, blue: 0.9882)   // #FFF4FC
        static let framboise97 = Color(red: 1.0000, green: 0.9765, blue: 0.9882)   // #FFF9FC
        static let mauve04 = Color(red: 0.0824, green: 0.0314, blue: 0.1569)   // #150828
        static let mauve08 = Color(red: 0.1059, green: 0.0784, blue: 0.1490)   // #1B1426
        static let mauve082 = Color(red: 0.1059, green: 0.0706, blue: 0.1882)   // #1B1230
        static let mauve10 = Color(red: 0.1451, green: 0.0588, blue: 0.2745)   // #250F46
        static let mauve11 = Color(red: 0.1686, green: 0.0667, blue: 0.2510)   // #2B1140
        static let mauve112 = Color(red: 0.1608, green: 0.0510, blue: 0.2863)   // #290D49
        static let mauve12 = Color(red: 0.1608, green: 0.0824, blue: 0.2784)   // #291547
        static let mauve122 = Color(red: 0.1686, green: 0.0863, blue: 0.2510)   // #2B1640
        static let mauve123 = Color(red: 0.1333, green: 0.1176, blue: 0.1882)   // #221E30
        static let mauve12Txt = Color(red: 0.7882, green: 0.6588, blue: 0.9608)   // #C9A8F5
        static let mauve13 = Color(red: 0.1333, green: 0.1137, blue: 0.2588)   // #221D42
        static let mauve17 = Color(red: 0.1804, green: 0.1529, blue: 0.2510)   // #2E2740
        static let mauve172 = Color(red: 0.1529, green: 0.1373, blue: 0.3529)   // #27235A
        static let mauve173 = Color(red: 0.1686, green: 0.1373, blue: 0.3216)   // #2B2352
        static let mauve18 = Color(red: 0.1608, green: 0.1412, blue: 0.3529)   // #29245A
        static let mauve182 = Color(red: 0.1765, green: 0.1490, blue: 0.3373)   // #2D2656
        static let mauve20 = Color(red: 0.2275, green: 0.1647, blue: 0.2431)   // #3A2A3E
        static let mauve23 = Color(red: 0.2392, green: 0.2000, blue: 0.3216)   // #3D3352
        static let mauve24 = Color(red: 0.2510, green: 0.1765, blue: 0.4157)   // #402D6A
        static let mauve28 = Color(red: 0.3020, green: 0.1765, blue: 0.5451)   // #4D2D8B
        static let mauve33 = Color(red: 0.1922, green: 0.2275, blue: 0.7647)   // #313AC3
        static let mauve35 = Color(red: 0.3647, green: 0.2863, blue: 0.4706)   // #5D4978
        static let mauve36 = Color(red: 0.1843, green: 0.2431, blue: 0.8392)   // #2F3ED6
        static let mauve39 = Color(red: 0.4275, green: 0.2392, blue: 0.7725)   // #6D3DC5
        static let mauve40 = Color(red: 0.3686, green: 0.2588, blue: 0.8275)   // #5E42D3
        static let mauve41 = Color(red: 0.4196, green: 0.3020, blue: 0.6784)   // #6B4DAD
        static let mauve47 = Color(red: 0.5059, green: 0.3333, blue: 0.7843)   // #8155C8
        static let mauve50 = Color(red: 0.4588, green: 0.4431, blue: 0.4980)   // #75717F
        static let mauve52 = Color(red: 0.5608, green: 0.3843, blue: 0.8196)   // #8F62D1
        static let mauve522 = Color(red: 0.6902, green: 0.2941, blue: 0.8235)   // #B04BD2
        static let mauve54 = Color(red: 0.5373, green: 0.4196, blue: 0.8275)   // #896BD3
        static let mauve58 = Color(red: 0.7490, green: 0.3529, blue: 0.8980)   // #BF5AE5
        static let mauve59 = Color(red: 0.5333, green: 0.4627, blue: 0.9725)   // #8876F8
        static let mauve62 = Color(red: 0.7961, green: 0.4510, blue: 0.6824)   // #CB73AE
        static let mauve63 = Color(red: 0.1608, green: 0.0824, blue: 0.2784)   // #291547
        static let mauve63Txt = Color(red: 0.1608, green: 0.0824, blue: 0.2784)   // #291547
        static let mauve64 = Color(red: 0.6667, green: 0.5020, blue: 0.9176)   // #AA80EA
        static let mauve69 = Color(red: 0.6980, green: 0.5804, blue: 0.9059)   // #B294E7
        static let mauve692 = Color(red: 0.6941, green: 0.5804, blue: 0.8902)   // #B194E3
        static let mauve73 = Color(red: 0.7373, green: 0.6157, blue: 0.9333)   // #BC9DEE
        static let mauve74 = Color(red: 0.7529, green: 0.6275, blue: 0.9608)   // #C0A0F5
        static let mauve75 = Color(red: 0.7686, green: 0.6353, blue: 0.9608)   // #C4A2F5
        static let mauve77 = Color(red: 0.7882, green: 0.6588, blue: 0.9608)   // #C9A8F5
        static let mauve77Txt = Color(red: 0.7882, green: 0.6588, blue: 0.9608)   // #C9A8F5
        static let mauve80 = Color(red: 0.8039, green: 0.7059, blue: 0.9647)   // #CDB4F6
        static let mauve84 = Color(red: 0.7961, green: 0.7804, blue: 0.8431)   // #CBC7D7
        static let mauve86 = Color(red: 0.9020, green: 0.8471, blue: 0.9804)   // #E6D8FA
        static let mauve90 = Color(red: 0.8706, green: 0.8549, blue: 0.9020)   // #DEDAE6
        static let mauve92 = Color(red: 0.9059, green: 0.8824, blue: 0.9333)   // #E7E1EE
        static let mauve94 = Color(red: 0.9333, green: 0.8941, blue: 0.9725)   // #EEE4F8
        static let mauve95 = Color(red: 0.9294, green: 0.9137, blue: 0.9608)   // #EDE9F5
        static let menthe11 = Color(red: 0.0000, green: 0.2039, blue: 0.1020)   // #00341A
        static let menthe15 = Color(red: 0.0745, green: 0.1686, blue: 0.1059)   // #132B1B
        static let menthe27 = Color(red: 0.1176, green: 0.2863, blue: 0.1725)   // #1E492C
        static let menthe58 = Color(red: 0.3451, green: 0.6078, blue: 0.3882)   // #589B63
        static let menthe59 = Color(red: 0.3608, green: 0.6078, blue: 0.4392)   // #5C9B70
        static let menthe67 = Color(red: 0.0000, green: 0.2039, blue: 0.1020)   // #00341A
        static let menthe67Txt = Color(red: 0.0000, green: 0.2039, blue: 0.1020)   // #00341A
        static let menthe72 = Color(red: 0.5020, green: 0.7529, blue: 0.5843)   // #80C095
        static let menthe722 = Color(red: 0.5843, green: 0.7294, blue: 0.5490)   // #95BA8C
        static let menthe82 = Color(red: 0.5608, green: 0.8784, blue: 0.5608)   // #8FE08F
        static let menthe87 = Color(red: 0.7569, green: 0.8902, blue: 0.8000)   // #C1E3CC
        static let menthe96 = Color(red: 0.8941, green: 0.9804, blue: 0.9137)   // #E4FAE9
        static let noir00 = Color(red: 0.0000, green: 0.0000, blue: 0.0000)   // #000000
        static let noir01 = Color(red: 0.0196, green: 0.0196, blue: 0.0196)   // #050505
        static let noir012 = Color(red: 0.0118, green: 0.0118, blue: 0.0275)   // #030307
        static let noir02 = Color(red: 0.0314, green: 0.0353, blue: 0.0471)   // #08090C
        static let noir03 = Color(red: 0.0431, green: 0.0471, blue: 0.0588)   // #0B0C0F
        static let orange34 = Color(red: 0.5451, green: 0.2000, blue: 0.1569)   // #8B3328
        static let orange40 = Color(red: 0.6706, green: 0.2157, blue: 0.1608)   // #AB3729
        static let orange402 = Color(red: 0.7255, green: 0.1294, blue: 0.1412)   // #B92124
        static let orange41 = Color(red: 0.6824, green: 0.2235, blue: 0.1608)   // #AE3929
        static let orange42 = Color(red: 0.9412, green: 0.4784, blue: 0.1804)   // #F07A2E
        static let orange43 = Color(red: 0.7137, green: 0.2314, blue: 0.1686)   // #B63B2B
        static let orange50 = Color(red: 0.8667, green: 0.2235, blue: 0.2157)   // #DD3937
        static let orange53 = Color(red: 0.8667, green: 0.3020, blue: 0.1373)   // #DD4D23
        static let orange53Txt = Color(red: 0.8667, green: 0.3020, blue: 0.1373)   // #DD4D23
        static let orange58 = Color(red: 0.8118, green: 0.4392, blue: 0.3725)   // #CF705F
        static let orange59 = Color(red: 0.9961, green: 0.3137, blue: 0.0000)   // #FE5000
        static let orangeMaParole = Color(red: 0.9843, green: 0.2980, blue: 0.0510)   // #FB4C0D — les mots « Ma Parole ! » des murs, et rien d'autre
        static let orangeMaParoleCorps = Color(red: 1.0000, green: 0.4784, blue: 0.3333)   // #FF7A55 — les mêmes, sur les corps sombres de Peaufiner (Chiche, Cercle)
        static let orangeMaParoleCobalt = Color(red: 0.9961, green: 0.8157, blue: 0.7647)   // #FED0C3 — le même orange, éclairci à 3:1 sur le corps bleu #0E78F2 d'un Promi (v134)
        static let orange61 = Color(red: 0.9098, green: 0.4392, blue: 0.2353)   // #E8703C
        static let orange62 = Color(red: 0.8784, green: 0.4706, blue: 0.4275)   // #E0786D
        static let orange64 = Color(red: 0.8392, green: 0.5412, blue: 0.3098)   // #D68A4F
        static let orange69 = Color(red: 0.8824, green: 0.5882, blue: 0.4314)   // #E1966E
        static let orange77 = Color(red: 0.9608, green: 0.6745, blue: 0.6196)   // #F5AC9E
        static let periwinkle53 = Color(red: 0.7725, green: 0.5843, blue: 0.3216)   // #C59552
        static let prune09 = Color(red: 0.1686, green: 0.0627, blue: 0.1255)   // #2B1020
        static let seiche10 = Color(red: 0.0196, green: 0.0118, blue: 0.0078)   // #050302
        static let seiche21 = Color(red: 0.1216, green: 0.0863, blue: 0.0667)   // #1F1611
        static let ton03 = Color(red: 0.0588, green: 0.0706, blue: 0.0824)   // #0F1215
        static let ton032 = Color(red: 0.0431, green: 0.0588, blue: 0.0706)   // #0B0F12
        static let ton07 = Color(red: 0.0510, green: 0.1216, blue: 0.2000)   // #0D1F33
        static let ton072 = Color(red: 0.0078, green: 0.1255, blue: 0.2235)   // #022039
        static let ton073 = Color(red: 0.0902, green: 0.1137, blue: 0.1490)   // #171D26
        static let ton08 = Color(red: 0.0314, green: 0.1294, blue: 0.2157)   // #082137
        static let ton082 = Color(red: 0.0745, green: 0.1333, blue: 0.2078)   // #132235
        static let ton09 = Color(red: 0.0196, green: 0.1529, blue: 0.2627)   // #052743
        static let ton092 = Color(red: 0.0667, green: 0.1490, blue: 0.2275)   // #11263A
        static let ton093 = Color(red: 0.0745, green: 0.1490, blue: 0.2275)   // #13263A
        static let ton094 = Color(red: 0.0902, green: 0.1451, blue: 0.2118)   // #172536
        static let ton095 = Color(red: 0.0824, green: 0.1490, blue: 0.2235)   // #152639
        static let ton096 = Color(red: 0.0863, green: 0.1490, blue: 0.2275)   // #16263A
        static let ton097 = Color(red: 0.0824, green: 0.1412, blue: 0.2235)   // #152439
        static let ton10 = Color(red: 0.1922, green: 0.1373, blue: 0.1451)   // #312325
        static let ton11 = Color(red: 0.0863, green: 0.1686, blue: 0.2588)   // #162B42
        static let ton112 = Color(red: 0.0941, green: 0.1686, blue: 0.2471)   // #182B3F
        static let ton12 = Color(red: 0.0980, green: 0.1922, blue: 0.2902)   // #19314A
        static let ton122 = Color(red: 0.0980, green: 0.1882, blue: 0.2980)   // #19304C
        static let ton13 = Color(red: 0.1059, green: 0.2000, blue: 0.2980)   // #1B334C
        static let ton132 = Color(red: 0.1137, green: 0.1961, blue: 0.2902)   // #1D324A
        static let ton133 = Color(red: 0.1098, green: 0.2039, blue: 0.3098)   // #1C344F
        static let ton134 = Color(red: 0.1020, green: 0.1961, blue: 0.3098)   // #1A324F
        static let ton14 = Color(red: 0.2941, green: 0.1765, blue: 0.1882)   // #4B2D30
        static let ton142 = Color(red: 0.1137, green: 0.2118, blue: 0.3176)   // #1D3651
        static let ton143 = Color(red: 0.1176, green: 0.2118, blue: 0.3176)   // #1E3651
        static let ton15 = Color(red: 0.1882, green: 0.2275, blue: 0.2980)   // #303A4C
        static let ton16 = Color(red: 0.3255, green: 0.2000, blue: 0.2118)   // #533336
        static let ton162 = Color(red: 0.1961, green: 0.2392, blue: 0.3020)   // #323D4D
        static let ton54 = Color(red: 0.6824, green: 0.7255, blue: 0.7961)   // #AEB9CB
        static let ton66 = Color(red: 0.7608, green: 0.7765, blue: 0.8039)   // #C2C6CD
        static let ton67 = Color(red: 0.5725, green: 0.8235, blue: 0.8196)   // #92D2D1
        static let ton82 = Color(red: 0.9961, green: 0.8157, blue: 0.6471)   // #FED0A5
        static let ton90 = Color(red: 0.8118, green: 0.8980, blue: 0.9961)   // #CFE5FE
    }
}
