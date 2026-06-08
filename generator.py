import re

def latex_to_revealjs(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Expresiones regulares para capturar la estructura definida
    topic_pattern = r'\\topic\{(.*?)\}'
    slide_pattern = r'\\slidetitle\{(.*?)\}\s*\\begin\{itemize\}(.*?)\\end\{itemize\}'
    
    # Inicio del HTML con Reveal.js y estilos inspirados en Precision_Medical_Ozone_Science.pdf
    html_start = """
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Presentación Medicina de Precisión</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/theme/black.min.css">
        <style>
            :root {
                --main-glow: #00d4ff;
                --text-bright: #ffffff;
            }
            .reveal h1, .reveal h2 {
                font-weight: bold;
                text-transform: uppercase;
                color: var(--main-glow);
                text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
            }
            .reveal .slides section {
                text-align: left;
                background: radial-gradient(circle at top right, #1a1a2e, #0d0d1a);
                border-left: 5px solid var(--main-glow);
                padding-left: 20px;
            }
            .reveal ul {
                list-style-type: none;
            }
            .reveal ul li::before {
                content: "•";
                color: var(--main-glow);
                display: inline-block;
                width: 1em;
                margin-left: -1em;
            }
            .topic-slide h1 { color: #ffffff !important; }
        </style>
    </head>
    <body>
        <div class="reveal">
            <div class="slides">
    """

    # Procesar Secciones (Topics) y Diapositivas
    slides_html = ""
    
    # Dividir el contenido por temas
    sections = re.split(r'\\topic', content)
    for section in sections:
        if not section.strip(): continue
        
        # Extraer el título del tema
        topic_match = re.search(r'\{(.*?)\}', section)
        if topic_match:
            slides_html += f'<section class="topic-slide"><h1>{topic_match.group(1)}</h1></section>\n'
        
        # Extraer cada slide dentro del tema
        slides = re.findall(slide_pattern, section, re.DOTALL)
        for title, body in slides:
            items = re.findall(r'\\item\s*(.*)', body)
            list_items = "".join([f'<li>{item.strip()}</li>' for item in items])
            
            slides_html += f"""
            <section>
                <h2>{title}</h2>
                <ul>
                    {list_items}
                </ul>
            </section>
            """

    html_end = """
            </div>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.js"></script>
        <script>
            Reveal.initialize({
                hash: true,
                center: true,
                transition: 'fade'
            });
        </script>
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_start + slides_html + html_end)
    print(f"¡Éxito! Archivo {output_file} generado.")

# Ejecución
if __name__ == "__main__":
    latex_to_revealjs('documento.tex', 'presentacion.html')