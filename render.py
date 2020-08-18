import markdown2
import functools

from os import listdir
from os.path import isfile, join


def load_template(template_path) -> callable:
    template_data = ""
    with open(template_path, 'r') as template_file:
        template_data = template_file.read()

    def apply_template() -> str:
        return template_data

    return apply_template


def table_of_contents(links_list: list) -> callable:
    links = ['[{}]({})'.format(l['text'], l['href']) for l in links_list]
    links = ' | '.join(links)
    links = markdown2.markdown(links)

    def apply_table_of_contents() -> str:
        return "\n\n{links}\n\n".format(links=links) + "{}"

    return apply_table_of_contents


def load_markdown(markdown_filename) -> callable:
    markdown_data = ""
    with open(markdown_filename) as infile:
        markdown_data = markdown2.markdown(infile.read())

    def apply_markdown() -> str:
        return markdown_data

    return apply_markdown


def apply_thing(a, b):
    return a.format(b())


def markdown_is_valid(directory_path, f, skip):
    return isfile(join(directory_path, f)) and f.split('.')[-1] == 'md' and f not in skip


def process_directory(directory_path='.', skip={'README.md', }):
    markdowns = [f for f in listdir(directory_path) if markdown_is_valid(directory_path, f, skip)]
    links = [{'text': f.replace('.md', '').title(), 'href': f.replace('.md', '.html')} for f in markdowns]
    for markdown in markdowns:
        data_pipeline = [
            load_template('template.html'),
            table_of_contents(links),
            load_markdown(markdown)
        ]
        with open(markdown.replace('.md', '.html'), 'w') as outfile:
            outfile.write(functools.reduce(apply_thing, data_pipeline, "{}"))


if __name__ == "__main__":
    process_directory()
