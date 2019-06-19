# DETImotic (website)

## Introduction
The project website describes the project and presents the system and team.

The project page can be accessed [here]().


## Installation
The page was generated using [Pelican](https://docs.getpelican.com/en/stable/quickstart.html) and Markdown was used to written the content.

1. Install Pelican
   
   `sudo apt-get install pelican`

2. Run the command:
   
   `pelican-quickstart`
  
3. Response some questions about configurations of the site. It is very easy to change these settings in the configuration file later (pelicanconf.py).
   
4. It's necessary clone of the repository in this page:
   
   `git clone https://github.com/getpelican/pelican-themes.git`
   
5. Next, clone of the repository in this page:

   `git clone https://github.com/getpelican/pelican-plugins.git`
6. Change the following fields accordingly:

   `THEME = '/home/user/git/pelican-themes/pelican-bootstrap3/'`
 
   `PLUGIN_PATHS = ['/home/user/git/pelican-plugins/']`

## Adding content

- All settings are made in file pelicanconfig.py that is generate for the pelican
- The images and pages are in directory called content
- Each component in navbar is a file on directory called pages
- To write the content on pages was used Markdown

## Execute locally for development

1. Open terminal in source page and insert this command line

   `make devserver`
2. Open browser (e.g. Firefox) and write:
   
   `localhost:8000`
   
## To publish
In folder the website:

`make ssh_upload`     


## Requirements
- All static files (HTML, Images, JS, CSS, etc…) files must belong to the group www-data so that the server can access those files.
