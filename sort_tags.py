'''
    This plugin adds tags_sorted_article_length to the context,
    which is a list of tupels (Tag, [Articles] which is sorted 
    by number of Articles first and Tag second.
    
    Usage:
    {% for tag, articles in tags_sorted_article_length %}
'''

from operator import itemgetter
from pelican import signals



def sort_tags_by_articles_size(generator):
    '''
        dirty hack to save an iteration over all items
        where we find the largest amount of articles
        
        needed so we can sort via tag as well since reverse would brake that
    '''
    most_articles = 99999

    def extract_and_size(item):
        articles = itemgetter(1)(item)
        length = len(articles)
        tag_lower = (itemgetter(0)(item)).slug.lower()
        return (most_articles - len(articles), tag_lower)
    
    generator.context['tags_sorted_by_article_length'] = sorted(
        generator.tags.items(),
        key=extract_and_size,
        reverse=False)



def register():
    signals.article_generator_finalized.connect(sort_tags_by_articles_size)