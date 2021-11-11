from helper import *


def get_diff_count(result):
    """ Gets the edit type count of a diff 
    
    Parameters
    ----------
    result : dict
        The diff API response containing inserts,removes and changes made in a Wikipedia revision.
    Returns
    -------
    dict
        a dict containing a count of edit type occurence
    """
    sections_affected = set()
    for r in result['remove']:
        sections_affected.add(r["section"])
    for i in result['insert']:
        sections_affected.add(i["section"])
    for c in result['change']:
        sections_affected.add(c['prev']["section"])

    edit_types = {}
    for s in sections_affected:
        for r in result['remove']:
            if not edit_types.get('remove'):
                edit_types['remove'] = {'edit_types':{}}
            if r["section"] == s:
                prev_text = result["sections-prev"][r["section"]]
                prev_text = prev_text[r['offset']:r['offset']+r['size']].replace("\n", "\\n")
                is_edit_type_found,wikitext,edit_type = is_edit_type(prev_text,r['type'])
        
                #check if edit_type in edit types dictionary
                if edit_type in edit_types.get('remove').get('edit_types').keys() and is_edit_type:
                    edit_types['remove']['edit_types'][edit_type] += 1
                else:
                    edit_types['remove']['edit_types'][edit_type] = 0
                    if is_edit_type_found:
                        edit_types['remove']['edit_types'][edit_type] += 1

        for i in result['insert']:
            if not edit_types.get('insert'):
                edit_types['insert'] = {'edit_types':{}}
            if i["section"] == s:
                curr_text = result["sections-curr"][i["section"]]
                curr_text = curr_text[i['offset']:i['offset']+i['size']].replace("\n", "\\n")
                is_edit_type_found,wikitext,edit_type = is_edit_type(curr_text,i['type'])
                #check if edit_type in edit types dictionary
                if edit_type in edit_types.get('insert').get('edit_types').keys() and is_edit_type:
                    edit_types['insert']['edit_types'][edit_type] += 1
                else:
                    edit_types['insert']['edit_types'][edit_type] = 0
                    if is_edit_type_found:
                        edit_types['insert']['edit_types'][edit_type] += 1

        for c in result['change']:
            if not edit_types.get('change'):
                edit_types['change'] = {'edit_types':{}}
            if c["prev"]["section"] == s:
                prev_text = result["sections-prev"][c["prev"]["section"]]
                prev_text = prev_text[c["prev"]['offset']:c["prev"]['offset']+c["prev"]['size']].replace("\n", "\\n")
                curr_text = result["sections-curr"][c["curr"]["section"]]
                curr_text = curr_text[c["curr"]['offset']:c["curr"]['offset']+c["curr"]['size']].replace("\n", "\\n")
                is_edit_type_found,wikitext,edit_type = is_edit_type(prev_text,c['prev']['type'])
                #check if edit_type in edit types dictionary
                if edit_type in edit_types.get('change').get('edit_types').keys() and is_edit_type:
                    edit_types['change']['edit_types'][edit_type] += 1
                else:
                    edit_types['change']['edit_types'][edit_type] = 0
                    if is_edit_type_found:
                        edit_types['change']['edit_types'][edit_type] += 1

    return edit_types




if __name__=='__main__':
    result = requests.get('https://edit-types.wmcloud.org/api/v1/diff?lang=en&revid=979988715').json()['diff']
    print(get_diff_count(result))

















