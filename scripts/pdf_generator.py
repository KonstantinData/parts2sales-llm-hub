from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


def render_pdf(summary: dict, output_file="evals/report.pdf"):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")
    html_out = template.render(summary=summary)
    HTML(string=html_out).write_pdf(output_file)
    print(f"📄 PDF report written to {output_file}")
