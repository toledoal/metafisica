#!/usr/bin/env python3
"""Genera qualicmetaphysics.org en cada idioma: index.html (es) y en/, fr/, de/.

El texto de cada idioma vive en contenido/<idioma>.html (fragmento: h2/h3 con id, p, ul).
La traducción sigue los términos vinculantes de metafisica-cualica/traduccion/ (qualo, habence,
the appearing…); aquí sólo se arma la página. Uso: python3 build.py
"""
import html
import json
import os
import re

SITIO = "https://qualicmetaphysics.org"
AUTOR = "Alejandro Toledo Martínez"
IB = "https://www.independentbooks.site"
AMAZON_MX = "https://www.amazon.com.mx/dp/B0GD27N9B3"   # Kindle, edición española
AMAZON_US = "https://www.amazon.com/dp/B0GD67N2T9"      # impreso, edición española

IDIOMAS = {
    "es": dict(
        dir="", og_locale="es_ES", nombre="Español",
        titulo="Metafísica Cuálica", titulo_pag="Metafísica Cuálica - Alejandro Toledo Martínez",
        desc="Metafísica Cuálica: una ontología del aparecer construida sobre la noción del cualo — la tesis de que la cualidad del aparecer es ontológicamente primaria, y la lógica secundaria. Investigación de Alejandro Toledo Martínez.",
        og_desc="Una ontología del aparecer construida sobre la noción del cualo: la cualidad del aparecer como ontológicamente primaria, y la lógica como secundaria.",
        titular="Metafísica Cuálica: hacia una filosofía de la cualidad",
        og_img=f"{IB}/og/es-metafisica-cualica.jpg",
        nav=["Inicio", "Contenido", "Descargas", "Libros", "Contacto"],
        badge="NUEVO", subtitulo="Hacia una filosofía de la cualidad",
        hero_desc="Edición Principal disponible ahora en Amazon",
        botones=[("Comprar en Amazon", AMAZON_MX, "btn-primary"),
                 ("Descargar PDF Gratis", "/libro-principal-metafisica.pdf", "btn-secondary")],
        explorar="Explorar Contenido", indice="Contenido",
        libro_t="Metafísica Cuálica - Libro Edición Principal",
        libro_sub="Disponible en formato impreso y digital en Amazon, y como descarga gratuita",
        libro_btn=[("Versión impresa", AMAZON_US, "btn-primary"), ("Kindle", AMAZON_MX, "btn-secondary")],
        libros_t="Libros",
        libros=[("Metafísica Cuálica", f"{IB}/libros/metafisica-cualica/"),
                ("Teoría de los Umbrales", f"{IB}/libros/teoria-de-los-umbrales/")],
        ensayo_t="Ensayo inicial",
        ensayo=[("PDF en Español (Edición Anterior)", "/Metafísica cuálica.pdf"),
                ("PDF Download (English Edition)", "/Qualic Metaphysics.pdf")],
        contacto="Contacto", f_nombre="Nombre", f_email="Email", f_msg="Mensaje", f_enviar="Enviar Mensaje",
        pie="Todos los derechos reservados.", idioma_label="Idioma",
    ),
    "en": dict(
        dir="en", og_locale="en_US", nombre="English",
        titulo="Qualic Metaphysics", titulo_pag="Qualic Metaphysics — Alejandro Toledo Martínez",
        desc="Qualic Metaphysics: an ontology of appearing built on the notion of the qualo — the thesis that the quality of appearing is ontologically primary, and logic secondary. Research by Alejandro Toledo Martínez.",
        og_desc="An ontology of appearing built on the notion of the qualo: the quality of appearing as ontologically primary, and logic as secondary.",
        titular="Qualic Metaphysics: toward a philosophy of quality",
        og_img=f"{IB}/og/en-qualic-metaphysics.jpg",
        nav=["Home", "Contents", "Downloads", "Books", "Contact"],
        badge="NEW", subtitulo="Toward a philosophy of quality",
        hero_desc="The book is available in English, and in Spanish on Amazon",
        botones=[("Get the book", f"{IB}/en/books/qualic-metaphysics/", "btn-primary"),
                 ("Spanish edition on Amazon", AMAZON_MX, "btn-secondary")],
        explorar="Explore the contents", indice="Contents",
        libro_t="Qualic Metaphysics — the book",
        libro_sub="English edition at Independent Books; the Spanish edition in print and Kindle on Amazon",
        libro_btn=[("English edition", f"{IB}/en/books/qualic-metaphysics/", "btn-primary"),
                   ("Spanish edition (Amazon)", AMAZON_US, "btn-secondary")],
        libros_t="Books",
        libros=[("Qualic Metaphysics", f"{IB}/en/books/qualic-metaphysics/"),
                ("Theory of Thresholds", f"{IB}/en/books/theory-of-thresholds/")],
        ensayo_t="Earlier essay",
        ensayo=[("PDF in Spanish (earlier edition)", "/Metafísica cuálica.pdf"),
                ("PDF in English (earlier edition)", "/Qualic Metaphysics.pdf")],
        contacto="Contact", f_nombre="Name", f_email="Email", f_msg="Message", f_enviar="Send message",
        pie="All rights reserved.", idioma_label="Language",
    ),
    "fr": dict(
        dir="fr", og_locale="fr_FR", nombre="Français",
        titulo="Métaphysique cualique", titulo_pag="Métaphysique cualique — Alejandro Toledo Martínez",
        desc="Métaphysique cualique : une ontologie de l’apparaître bâtie sur la notion de cualo — la thèse selon laquelle la qualité de l’apparaître est ontologiquement première, et la logique seconde. Recherche d’Alejandro Toledo Martínez.",
        og_desc="Une ontologie de l’apparaître bâtie sur la notion de cualo : la qualité de l’apparaître comme ontologiquement première, et la logique comme seconde.",
        titular="Métaphysique cualique : vers une philosophie de la qualité",
        og_img=f"{IB}/og/en-qualic-metaphysics.jpg",
        nav=["Accueil", "Sommaire", "Téléchargements", "Livres", "Contact"],
        badge="NOUVEAU", subtitulo="Vers une philosophie de la qualité",
        hero_desc="Le livre existe en anglais et en espagnol",
        botones=[("Édition anglaise", f"{IB}/en/books/qualic-metaphysics/", "btn-primary"),
                 ("Édition espagnole sur Amazon", AMAZON_MX, "btn-secondary")],
        explorar="Explorer le texte", indice="Sommaire",
        libro_t="Métaphysique cualique — le livre",
        libro_sub="Édition anglaise chez Independent Books ; édition espagnole imprimée et Kindle sur Amazon",
        libro_btn=[("Édition anglaise", f"{IB}/en/books/qualic-metaphysics/", "btn-primary"),
                   ("Édition espagnole (Amazon)", AMAZON_US, "btn-secondary")],
        libros_t="Livres",
        libros=[("Qualic Metaphysics (anglais)", f"{IB}/en/books/qualic-metaphysics/"),
                ("Théorie des Seuils (anglais)", f"{IB}/en/books/theory-of-thresholds/")],
        ensayo_t="Essai initial",
        ensayo=[("PDF en espagnol (édition antérieure)", "/Metafísica cuálica.pdf"),
                ("PDF en anglais (édition antérieure)", "/Qualic Metaphysics.pdf")],
        contacto="Contact", f_nombre="Nom", f_email="E-mail", f_msg="Message", f_enviar="Envoyer le message",
        pie="Tous droits réservés.", idioma_label="Langue",
    ),
    "de": dict(
        dir="de", og_locale="de_DE", nombre="Deutsch",
        titulo="Qualische Metaphysik", titulo_pag="Qualische Metaphysik — Alejandro Toledo Martínez",
        desc="Qualische Metaphysik: eine Ontologie des Erscheinens, gebaut auf dem Begriff des Qualo — der These, dass die Qualität des Erscheinens ontologisch primär ist und die Logik sekundär. Forschung von Alejandro Toledo Martínez.",
        og_desc="Eine Ontologie des Erscheinens, gebaut auf dem Begriff des Qualo: die Qualität des Erscheinens als ontologisch primär, die Logik als sekundär.",
        titular="Qualische Metaphysik: auf dem Weg zu einer Philosophie der Qualität",
        og_img=f"{IB}/og/en-qualic-metaphysics.jpg",
        nav=["Start", "Inhalt", "Downloads", "Bücher", "Kontakt"],
        badge="NEU", subtitulo="Auf dem Weg zu einer Philosophie der Qualität",
        hero_desc="Das Buch gibt es auf Englisch und auf Spanisch",
        botones=[("Englische Ausgabe", f"{IB}/en/books/qualic-metaphysics/", "btn-primary"),
                 ("Spanische Ausgabe bei Amazon", AMAZON_MX, "btn-secondary")],
        explorar="Zum Text", indice="Inhalt",
        libro_t="Qualische Metaphysik — das Buch",
        libro_sub="Englische Ausgabe bei Independent Books; spanische Ausgabe gedruckt und als Kindle bei Amazon",
        libro_btn=[("Englische Ausgabe", f"{IB}/en/books/qualic-metaphysics/", "btn-primary"),
                   ("Spanische Ausgabe (Amazon)", AMAZON_US, "btn-secondary")],
        libros_t="Bücher",
        libros=[("Qualic Metaphysics (englisch)", f"{IB}/en/books/qualic-metaphysics/"),
                ("Theorie der Schwellen (englisch)", f"{IB}/en/books/theory-of-thresholds/")],
        ensayo_t="Früher Essay",
        ensayo=[("PDF auf Spanisch (frühere Ausgabe)", "/Metafísica cuálica.pdf"),
                ("PDF auf Englisch (frühere Ausgabe)", "/Qualic Metaphysics.pdf")],
        contacto="Kontakt", f_nombre="Name", f_email="E-Mail", f_msg="Nachricht", f_enviar="Nachricht senden",
        pie="Alle Rechte vorbehalten.", idioma_label="Sprache",
    ),
}


# Recuadro al inicio del texto: el cualo no es el quale de la filosofía de la mente.
# es / en: palabras del capítulo 5 del libro («Advertencia terminológica»); fr / de: traducción con los términos fijados.
QUALIA = {
    "es": dict(t="Cualo, no qualia", fuente="— <em>Metafísica cuálica</em>, capítulo 5", p=[
        "En filosofía de la mente, <em>qualia</em> suele implicar marcos representacionales y psicologistas que aquí <strong>no adoptamos</strong>. Nuestra pregunta no es la misma: no buscamos un «objeto mental privado» que la ciencia no pueda medir. Buscamos delimitar el estatuto ontológico del <em>aparecer</em> y su relación con la articulación (<em>logos</em>).",
        "Un <strong>cualo</strong> es una unidad irreductible de aparecer vivido en el campo de la habencia, previa a la articulación conceptual, lingüística y proposicional.",
        "Por eso decimos <em>cualo</em> y no <em>quale</em>: <em>qualia</em> aparece únicamente como término técnico histórico, cuando es inevitable, y siempre con esta advertencia."]),
    "en": dict(t="Qualo, not qualia", fuente="— <em>Qualic Metaphysics</em>, chapter 5", p=[
        "In philosophy of mind, <em>qualia</em> usually implies representational and psychologistic frameworks that here we <strong>do not adopt</strong>. Our question is not the same: we are not looking for a “private mental object” that science cannot measure. We are looking to delimit the ontological status of <em>appearing</em> and its relation to articulation (<em>logos</em>).",
        "A <strong>qualo</strong> is an irreducible unit of lived appearing in the field of habence, prior to conceptual, linguistic and propositional articulation.",
        "That is why we say <em>qualo</em> and not <em>quale</em>: <em>qualia</em> appears solely as a historical technical term when unavoidable, and always with this warning."]),
    "fr": dict(t="Cualo, et non qualia", fuente="— d’après le livre, chapitre\u00a05", p=[
        "En philosophie de l’esprit, les <em>qualia</em> impliquent d’ordinaire des cadres représentationnels et psychologistes que nous <strong>n’adoptons pas</strong> ici. Notre question n’est pas la même\u202f: nous ne cherchons pas un «\u00a0objet mental privé\u00a0» que la science ne pourrait pas mesurer. Nous cherchons à délimiter le statut ontologique de l’<em>apparaître</em> et son rapport à l’articulation (<em>logos</em>).",
        "Un <strong>cualo</strong> est une unité irréductible d’apparaître vécu dans le champ de l’habence, antérieure à l’articulation conceptuelle, linguistique et propositionnelle.",
        "C’est pourquoi nous disons <em>cualo</em> et non <em>quale</em>\u00a0: le terme <em>qualia</em> n’apparaît que comme terme technique historique, lorsqu’il est inévitable, et toujours avec cet avertissement."]),
    "de": dict(t="Qualo, nicht Qualia", fuente="— nach dem Buch, Kapitel 5", p=[
        "In der Philosophie des Geistes impliziert <em>Qualia</em> meist repräsentationale und psychologistische Rahmen, die wir hier <strong>nicht übernehmen</strong>. Unsere Frage ist nicht dieselbe: Wir suchen kein „privates mentales Objekt“, das die Wissenschaft nicht messen kann. Wir wollen den ontologischen Status des <em>Erscheinens</em> und sein Verhältnis zur Artikulation (<em>Logos</em>) bestimmen.",
        "Ein <strong>Qualo</strong> ist eine irreduzible Einheit gelebten Erscheinens im Feld der Habenz, vor jeder begrifflichen, sprachlichen und propositionalen Artikulation.",
        "Darum sagen wir <em>Qualo</em> und nicht <em>Quale</em>: <em>Qualia</em> erscheint nur als historischer Fachbegriff, wo es unvermeidlich ist, und immer mit diesem Hinweis."]),
}


def url(cod):
    d = IDIOMAS[cod]["dir"]
    return f"{SITIO}/{d + '/' if d else ''}"


def disponibles():
    return [c for c in IDIOMAS if os.path.exists(f"contenido/{c}.html")]


def e(t):
    return html.escape(t, quote=True)


def pagina(cod, langs):
    L = IDIOMAS[cod]
    art = open(f"contenido/{cod}.html", encoding="utf-8").read().strip()
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>'
                  for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', art))
    alternos = "\n".join(f'    <link rel="alternate" hreflang="{c}" href="{url(c)}">' for c in langs)
    alternos += f'\n    <link rel="alternate" hreflang="x-default" href="{url("es")}">'
    selector = " ".join(
        f'<span class="lang-actual" aria-current="true">{c.upper()}</span>' if c == cod
        else f'<a href="{url(c)}" hreflang="{c}" lang="{c}" title="{IDIOMAS[c]["nombre"]}">{c.upper()}</a>'
        for c in langs)
    autor = {"@type": "Person", "@id": f"{SITIO}/#autor", "name": AUTOR,
             "sameAs": [f"{IB}/", "https://www.endolinguistics.science/", "https://www.endolinguistica.com/"]}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{SITIO}/#web", "url": f"{SITIO}/", "name": IDIOMAS["es"]["titulo"],
         "inLanguage": langs, "publisher": {"@id": f"{SITIO}/#autor"}},
        autor,
        {"@type": "Article", "headline": L["titular"], "inLanguage": cod, "author": {"@id": f"{SITIO}/#autor"},
         "mainEntityOfPage": url(cod), "image": L["og_img"],
         "about": ["metaphysics", "quality", "qualo", "ontology", "habence", "Agustín Basave Fernández del Valle"]},
        {"@type": "Book", "name": "Metafísica Cuálica", "author": {"@id": f"{SITIO}/#autor"}, "inLanguage": "es",
         "url": f"{IB}/libros/metafisica-cualica/", "image": f"{IB}/og/es-metafisica-cualica.jpg",
         "sameAs": [AMAZON_MX, AMAZON_US],
         "workTranslation": {"@type": "Book", "name": "Qualic Metaphysics", "inLanguage": "en",
                             "url": f"{IB}/en/books/qualic-metaphysics/"}}]}
    nav = "".join(f'<li><a href="#{a}">{t}</a></li>'
                  for a, t in zip(["inicio", "contenido", "descargas", "libros", "contacto"], L["nav"]))
    botones = "\n".join(
        f'                    <a href="{h}"{" download" if h.endswith(".pdf") else " target=\"_blank\" rel=\"noopener noreferrer\""} class="btn {c}">{e(t)}</a>'
        for t, h, c in L["botones"])
    libro_btn = "\n".join(
        f'                    <a href="{h}" target="_blank" rel="noopener noreferrer" class="btn {c} btn-book">{e(t)}</a>'
        for t, h, c in L["libro_btn"])
    sep = '\n                    <span class="separator">•</span>\n'
    libros = sep.join(f'                    <a href="{h}" class="download-link-simple">{e(t)}</a>' for t, h in L["libros"])
    ensayo = sep.join(f'                    <a href="{h}" download class="download-link-simple">{e(t)}</a>' for t, h in L["ensayo"])
    return f"""<!DOCTYPE html>
<html lang="{cod}">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{e(L["titulo_pag"])}</title>
    <meta name="description" content="{e(L["desc"])}">
    <meta name="author" content="{AUTOR}">
    <link rel="canonical" href="{url(cod)}">
{alternos}
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:locale" content="{L["og_locale"]}">
    <meta property="og:site_name" content="{e(L["titulo"])}">
    <meta property="og:title" content="{e(L["titulo"])}">
    <meta property="og:description" content="{e(L["og_desc"])}">
    <meta property="og:url" content="{url(cod)}">
    <meta property="og:image" content="{L["og_img"]}">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&display=swap"
        rel="stylesheet">
    <!-- Foundation CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/foundation-sites@6.8.1/dist/css/foundation.min.css">
    <link rel="stylesheet" href="/styles.css">
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-GHKYD3THD3"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-GHKYD3THD3');
    </script>
</head>

<body>
    <!-- Navigation -->
    <nav class="main-nav">
        <div class="grid-container">
            <div class="grid-x grid-padding-x align-middle">
                <div class="cell auto">
                    <div class="nav-brand">{e(L["titulo"])}</div>
                </div>
                <div class="cell shrink">
                    <ul class="nav-menu">
                        {nav}
                    </ul>
                </div>
                <div class="cell shrink">
                    <div class="lang-switch" aria-label="{L["idioma_label"]}">{selector}</div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <header id="inicio" class="hero-section">
        <div class="grid-container">
            <div class="text-center">
                <span class="hero-badge">{L["badge"]}</span>
                <h1 class="hero-title">{e(L["titulo"])}</h1>
                <p class="hero-subtitle">{e(L["subtitulo"])}</p>
                <p class="hero-description">{e(L["hero_desc"])}</p>
                <div class="hero-buttons">
{botones}
                    <a href="#contenido" class="btn btn-text">{e(L["explorar"])}</a>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main id="contenido">
        <article id="content-container" class="articulo">
            <aside class="aviso-qualia" id="{"qualo-qualia"}">
                <h2>{QUALIA[cod]["t"]}</h2>
{"".join(f"                <p>{x}</p>" + chr(10) for x in QUALIA[cod]["p"])}                <p class="aviso-fuente">{QUALIA[cod]["fuente"]}</p>
            </aside>
            <nav class="indice" aria-label="{e(L["indice"])}">
                <h2>{e(L["indice"])}</h2>
                <ol>{toc}</ol>
            </nav>
{art}
        </article>
    </main>

    <!-- New Book Highlight Section -->
    <section class="new-book-section">
        <div class="grid-container">
            <div class="text-center">
                <h2 class="section-title">{e(L["libro_t"])}</h2>
                <p class="section-subtitle">{e(L["libro_sub"])}</p>
                <div class="book-links">
{libro_btn}
                </div>
            </div>
        </div>
    </section>

    <!-- Books Section -->
    <section id="libros" class="downloads-section">
        <div class="grid-container">
            <div class="text-center">
                <h2 class="section-title">{e(L["libros_t"])}</h2>
                <div class="download-links-simple">
{libros}
                </div>
            </div>
        </div>
    </section>

    <!-- Downloads Section -->
    <section id="descargas" class="downloads-section">
        <div class="grid-container">
            <div class="text-center">
                <h2 class="section-title">{e(L["ensayo_t"])}</h2>
                <div class="download-links-simple">
{ensayo}
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Form -->
    <section id="contacto" class="contact-section">
        <div class="grid-container">
            <h2 class="section-title text-center">{e(L["contacto"])}</h2>
            <form action="https://formspree.io/f/mjkwbpyz" method="POST" class="contact-form">
                <div class="form-group">
                    <label for="name">{e(L["f_nombre"])}</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="email">{e(L["f_email"])}</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="message">{e(L["f_msg"])}</label>
                    <textarea id="message" name="message" rows="5" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary btn-block">{e(L["f_enviar"])}</button>
            </form>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="grid-container">
            <p class="footer-text text-center">&copy; 2025 {AUTOR}. {e(L["pie"])}</p>
        </div>
    </footer>

    <!-- Foundation JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/foundation-sites@6.8.1/dist/js/foundation.min.js"></script>
    <script>
        $(document).foundation();
    </script>
</body>

</html>
"""


def sitemap(langs):
    urls = []
    for c in langs:
        alt = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{o}" href="{url(o)}"/>' for o in langs)
        urls.append(f"""  <url>
    <loc>{url(c)}</loc>
    <lastmod>2026-09-30</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if c == "es" else "0.9"}</priority>{alt}
  </url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def main():
    langs = disponibles()
    for c in langs:
        d = IDIOMAS[c]["dir"]
        if d:
            os.makedirs(d, exist_ok=True)
        out = os.path.join(d, "index.html") if d else "index.html"
        open(out, "w", encoding="utf-8").write(pagina(c, langs))
        print(f"{out}: {c}")
    open("sitemap.xml", "w", encoding="utf-8").write(sitemap(langs))
    print(f"sitemap.xml: {len(langs)} idiomas")


if __name__ == "__main__":
    main()
