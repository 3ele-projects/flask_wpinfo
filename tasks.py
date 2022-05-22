import requests
import models.WpInfo  as Wp
import models.TechnicalInfo as TI
import urllib.parse
def create_task(domain):

    parsed_url = urllib.parse.urlparse(domain)

  #  technical_info = TI.TechnicalInfo(domain, parsed_url)
  #  technical_info.run()
    wp_info = Wp.WpInfo()
    wp_info.posts = wp_info.get_all_posts(domain, 'posts') 
    wp_info.users = wp_info.get_all_posts(domain, 'users') 
    
    wp_info.pages = wp_info.get_all_posts(domain, 'pages') 
    wp_info.login_page = wp_info.get_admin_url(domain)
    wp_info.types = list()
    for type in  wp_info.get_all_posts(domain, 'types')['posts']:     
        my_type = dict()
        my_type['name'] = type
        my_type['content'] = wp_info.get_all_posts(domain, type)
        wp_info.types.append(my_type)
       
       


    wp_info.posts['nwst'] = {}
    wp_info.posts['oldest'] = {}
    wp_info.pages['nwst'] = {}
    wp_info.pages['oldest'] = {}

    wp_info.posts['nwst']['modified'] = wp_info.get_nwst(wp_info.get_all_posts(domain, 'posts'),'modified')
    wp_info.pages['oldest']['modified'] = wp_info.get_oldest(wp_info.get_all_posts(domain, 'pages'),'modified')
    wp_info.posts['nwst']['date'] = wp_info.get_nwst(wp_info.get_all_posts(domain, 'posts'),'date')
    wp_info.pages['oldest']['date'] = wp_info.get_oldest(wp_info.get_all_posts(domain, 'pages'),'date')


    #wp_info = {
    #   "label" : 'System Informationen',
    #   "system" : 'Wordpress'
    #}

    customer = {
        "firstname" : 'Joel',
        "lastname": 'Burghardt'
    }



    json_data = {
     
        "domain" : domain,
     #   "technical_info" : technical_info.__dict__,
        "wp_info" : wp_info.__dict__,
   
    }

  
    return json_data