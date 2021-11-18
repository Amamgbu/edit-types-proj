import mwparserfromhell as mw
import requests



def getNamespacePrefixes(lang):
    session = requests.Session()
    base_url = "https://{0}.wikipedia.org/w/api.php".format(lang)
    params = {
        "action": "query",
        "meta": "siteinfo",
        "siprop": "namespacealiases|namespaces",
        "format": "json",
        "formatversion": "2"
    }
    result = session.get(url=base_url, params=params)
    result = result.json()
    prefix_to_ns = {}
   
    if 'namespacealiases' in result.get('query', {}):
        for alias in result['query']['namespacealiases']:
            prefix_to_ns[alias['alias']] = alias['id']
    if 'namespaces' in result.get('query', {}):
        for ns in result['query']['namespaces'].values():
            if 'name' in ns:
                prefix_to_ns[ns['name'].replace(' ', '_')] = ns['id']
            if 'canonical' in ns:
                prefix_to_ns[ns['canonical'].replace(' ', '_')] = ns['id']
    return prefix_to_ns

def filterLinksByNs(links, keep_ns):
    """ Filters wikilinks by namespaces
    
    Parameters
    ----------
    links : list
        List of Wikilinks
    keep_ns: list
        List of namespaces to filter by
    
    Returns
    -------
    links
        Filtered link
    """

    for i in range(len(links)-1, -1, -1):
        link_ns = 0
        if ':' in links[i]:
            prefix = links[i].split(':')[0].replace(' ', '_').replace('[[','') 
            if prefix in namespace_prefixes:
                link_ns = namespace_prefixes[prefix]
        if link_ns not in keep_ns:
            links.pop(i)
    return links



def is_edit_type(wikitext,node_type):
    """ Checks if wikitext is an edit type
    
    Parameters
    ----------
    wikitext : str
        Wikitext
    node_type: str
        Node type

    Returns
    -------
    tuple
        Tuple containing the bool,wikitext and edit type
    """
    parsed_text = mw.parse(wikitext)
    #If type field is Text
    if node_type == 'Text':
        text = parsed_text.filter_text()
        if len(text) > 0:
            return True,text[0],'Text'


    elif node_type == 'Tag':
        #Check if edit type is a reference
        ref = parsed_text.filter_tags(matches=lambda node: node.tag == "ref")
        if len(ref) > 0:
            return True,ref[0],'Reference'
        #Check if edit type is a table
        table = parsed_text.filter_tags(matches=lambda node: node.tag == "tables")
        if len(table) > 0:
            return True,table[0],'Table'

        #Check if edit type is a text formatting
        text_format = parsed_text.filter_tags()
        text_format = re.findall("'{2}.*''",str(text_format[0]))
        if len(text_format) > 0:
            return True,text_format[0],'Text Formatting'

    elif node_type == 'Comment':
        comment = parsed_text.filter_comments()
        if len(comments) > 0:
            return True,comments[0],'Comment'

    elif node_type == 'Template':
        templates = parsed_text.filter_templates()
        if len(templates) > 0:
            return True,templates[0],'Template'

    elif node_type == 'Heading':
        section = parsed_text.filter_heading()
        if len(section) > 0:
            return True,section[0],'Section'

    elif node_type == 'Wikilink':
        link = parsed_text.filter_wikilinks()
        #Check if edit type is a category or image or inlink
        if len(link) > 0:
        #Get copy of list
            wikilink_copy = link.copy()
            wikilink = filterLinksByNs(wikilink_copy,[0])

            cat_copy = link.copy()
            cat = filterLinksByNs(cat_copy,[14])
        
            image_copy = link.copy()
            image = filterLinksByNs(image_copy,[6])
        
        if len(cat) > 0:
            return True,cat[0],'Category'
        if len(image) > 0:
            return True,image[0],'Image'
        if len(wikilink) > 0:
            return True,wikilink[0],'Wikilink'

    elif node_type == 'ExternalLink':
        external_link = parsed_text.filter_external_links()
        if len(external_link) > 0:
            return True,external_link[0],'External Link'
    else:
        return False,None,None