import markdown2
from os import listdir
from os.path import isfile, join

def render_markdown(markdown_filename, output_filename, toc):
	print(markdown_filename, output_filename)
	with open(output_filename, 'w') as outfile:
		with open('head.html.fragment') as infile:
			outfile.write(infile.read())
		outfile.write('<p>{}</p>'.format(toc))
		with open(markdown_filename) as infile:
			outfile.write(markdown2.markdown(infile.read()))
		with open('tail.html.fragment') as infile:
			outfile.write(infile.read())


if __name__ == "__main__":
	mypath = '.'
	markdowns = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.split('.')[-1] == 'md' and f != 'README.md']
	links = ['<a href="/{}">{}</a>'.format(f.replace('.md', '.html'), f.replace('.md', '').title()) for f in markdowns]
	toc = ' | '.join(links)
	for file in markdowns:
		render_markdown(file, file.replace('.md', '.html'), toc)
