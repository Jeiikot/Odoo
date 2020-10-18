{
  'name':'Tutorial theme',
  'description': 'My first theme in Odoo',
  'version':'1.0',
  'author':'Odoo Tutorial',

  'data': [
    'views/layout.xml',
    'views/pages.xml'
  ],
  'category': 'Theme/Creative',
  'depends': ['website', 'website_theme_install', 'website_blog', 'sale'],
}