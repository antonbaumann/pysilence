import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name='pysilence',
	version='0.1.2',
	scripts=[],
	author="Anton Baumann",
	author_email="anton@antonbaumann.com",
	description="A silence detection module",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/antonbaumann/pysilence",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
