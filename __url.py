def Bookmark_url( id , page , hide = "show"):
    '''
    A function use to get the bookmark url
        id: Your Pixiv id
        page : the page number in the bookmark you want to get
        hide : default "show", use "hide" for hidden'''
    return 'https://www.pixiv.net/ajax/user/{}/illusts/bookmarks?tag=&offset={}&limit=48&rest={}&lang=zh'.format(id,(page*48),hide)


def Discovery_url(lim, mode = 'safe'):
    if(mode == 'safe'):
        return 'https://www.pixiv.net/ajax/discovery/artworks?mode=safe&limit={}&lang=zh'.format(lim)

    if(mode == 'all'):
        return 'https://www.pixiv.net/ajax/discovery/artworks?mode=all&limit={}&lang=zh'.format(lim)
    
    if(mode == 'r-18'):
        return 'https://www.pixiv.net/ajax/discovery/artworks?mode=r18&limit={}&lang=zh'.format(lim)

def BookmarkCount_url(id):
    return 'https://www.pixiv.net/ajax/illust/{}?lang=zh'.format(id)

def Recommend_url(id,lim):
    return "https://www.pixiv.net/ajax/illust/{}/recommend/init?limit={}&lang=zh".format(id,lim)

#def Illustrator_url(id, page):
#    return "https://www.pixiv.net/ajax/user/{}/profile/illusts?work_category=illust&is_first_page={}&lang=zh".format(id, page)

def Illustrator_url(id):
    return "https://www.pixiv.net/ajax/user/{}/profile/all?lang=zh".format(id)

def Search_url(keys):
    return