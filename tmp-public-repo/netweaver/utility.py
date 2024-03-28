"Utility module for NetWeaver"

""" =================================================================
| utility.py -- NetWeaver/netweaver/utility.py
|
| Created by Jack on 07/11/2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

from enum import Enum
from typing import *

__all__ = 'DesktopSize', 'MobileSize'


class DesktopSize(Enum):
    "Common desktop resolutions."
    
    SMALL   = (1024, 768)
    "Standard 4:3 aspect ratio."
    HD      = (1280, 720)
    "HD resolution, 16:9 aspect ratio."
    FHD     = (1920, 1080)
    "Full HD resolution, 16:9 aspect ratio."
    QHD     = (2560, 1440)
    "Quad HD resolution, 16:9 aspect ratio."
    ULTRAHD = (3840, 2160)
    "Ultra HD resolution, also known as 4K, 16:9 aspect ratio."
    UWHD    = (2560, 1080)
    "Ultra Wide HD resolution, 21:9 aspect ratio."
    UWFHD   = (3440, 1440)
    "Ultra Wide Full HD resolution, 21:9 aspect ratio."
    UWQHD   = (3440, 1440)
    "Duplicate of UWFHD, Ultra Wide Quad HD resolution, 21:9 aspect ratio."
    UHDPLUS = (5120, 2160)
    "Ultra Wide 5K resolution, wider than 4K for extra workspace."

class MobileSize(Enum):
    "Common mobile resolutions."
    
    STANDARD = (375, 667)
    "Standard iPhone resolution, common before iPhone 6."
    PLUS = (414, 736)
    "Plus iPhone resolution, used for larger iPhone models."
    XL = (412, 846)
    "XL size, slightly taller than Plus models."

    ANDROID_SMALL = (720, 1280)
    "Common smaller Android resolution."
    ANDROID_MEDIUM = (1080, 1920)
    "Common medium Android resolution."
    ANDROID_LARGE = (1440, 2560)
    "Common large Android resolution."
    GALAXYS10 = (1440, 3040)
    "Samsung Galaxy S10 resolution."
    GALAXYS20 = (1440, 3200)
    "Samsung Galaxy S20 resolution."
    PIXEL4 = (1080, 2280)
    "Google Pixel 4 resolution."
    PIXEL5 = (1080, 2340)
    "Google Pixel 5 resolution."

    RETINA_HD = (750, 1334)
    "Retina HD resolution, used for iPhone 6/6s/7/8."
    IPHONE11_12 = (828, 1792)
    "iPhone 11 and 12 standard resolution."
    IPHONE11PRO_12MINI = (1125, 2436)
    "iPhone 11 Pro and 12 Mini resolution."
    IPHONE11PROMAX_12PROMAX = (1242, 2688)
    "iPhone 11 Pro Max and 12 Pro Max resolution."
    IPHONE13MINI = (1080, 2340)
    "iPhone 13 Mini resolution."
    IPHONE13PRO = (1170, 2532)
    "iPhone 13 Pro resolution."
    IPHONE13PROMAX = (1284, 2778)
    "iPhone 13 Pro Max resolution."

    FHD_PLUS = (1080, 2340)
    "Full HD Plus resolution, common in newer high-end phones."
    
class Script:
    
    remove_element = lambda: '''
        console.log("Netweaver removing element ->", arguments[0]);
        var element = arguments[0];
        if (element && element.parentNode) {
            element.parentNode.removeChild(element);
        }
    '''
    
    focus = lambda: '''
        arguments[0].focus();
    '''
    
    set_timeout_callback = lambda callback, timeout: f"""
        setTimeout(() => {{
            {callback}
        }}, {timeout});
    """
    
    set_inline_style = lambda css: f'''
        arguments[0].setAttribute('style', "{css}");
    '''
    
    get_pseudo_elem_style = lambda computedStyle: f'''
        let pseudoElem = window.getComputedStyle(arguments[0], '::{computedStyle}');
        let styleObj = {{}};
        for (let prop of pseudoElem) {{
            styleObj[prop] = pseudoElem.getPropertyValue(prop);
        }}
        return styleObj;
    '''
    
    is_within_viewport = lambda: '''
        var rect = arguments[0].getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    '''
    
    get_direct_text_self = lambda shouldTrim: f'''
        return Array
            .from(arguments[0].childNodes)
            .filter(node => node.nodeType === 3) // getting textnode
            .map(node => {str(shouldTrim).lower()} ? node.nodeValue.trim() : node.nodeValue)
            .join(" ");
    '''
    
    get_direct_text_forward_lineage = lambda shouldTrim: f'''
        function getAllTextNodes(element) {{
            let nodes = [];
            for (let node of element.childNodes) {{
                if (node.nodeType === 3) {{
                    nodes.push(node);
                }} else if (node.nodeType === 1) {{
                    nodes = nodes.concat(getAllTextNodes(node));
                }}
            }}
            return nodes;
        }}
        
        return getAllTextNodes(arguments[0])
            .map(node => {str(shouldTrim).lower()} ? node.nodeValue.trim() : node.nodeValue)
            .join(" ");
    '''
    
    get_descendants_with_direct_text = lambda searchText, caseSensitive: f'''
        return (
            function findElementsWithDirectText(elem, searchText, caseSensitive) {{
                let matchedElements = [];

                let directText = Array.from(elem.childNodes).reduce((acc, node) => {{
                    if (node.nodeType === 3) acc += node.textContent;
                    return acc;
                }}, "").trim();

                if (!caseSensitive) {{
                    directText = directText.toLowerCase();
                    searchText = searchText.toLowerCase();
                }}

                if (directText === searchText) {{
                    matchedElements.push(elem);
                }} else {{
                    for (let child of elem.children) {{
                        matchedElements = matchedElements.concat(findElementsWithDirectText(child, searchText, caseSensitive));
                    }}
                }}

                return matchedElements;
            }}
        )(arguments[0], "{searchText}", {str(caseSensitive).lower()});
    '''
    
    has_pseduo_elem = lambda x : f'''
        let pseudoElem = window.getComputedStyle(arguments[0], '::{x}');
        return pseudoElem.getPropertyValue('content');
    '''
    
    get_attr_with_prefix = lambda startStr: f'''
        function getAttributesStartingWith(element, startStr) {{
            let attrs = {{}};
            Array.from(element.attributes).forEach(attr => {{
                if (attr.name.startsWith(startStr)) {{
                    attrs[attr.name] = attr.value;
                }}
            }});
            return attrs;
        }}
        return getAttributesStartingWith(arguments[0], "{startStr}");
    '''
    
    scroll_to_window_scrollHeight = lambda: '''
        window.scrollTo(0, document.body.scrollHeight);
    '''
    
    scroll_element_into_view_offsetXY = lambda x, y: f'''
        arguments[0].scrollIntoView();
        window.scrollBy({x}, {y});
    '''
    
    scroll_to_element_scrollHeight = lambda: '''
        arguments[0].scrollTop = arguments[0].scrollHeight;
    '''
    
    get_element_scrollTop = lambda: '''
        return arguments[0].scrollTop;
    '''
    "get the current scrollTop position of the WebElement"
    
    get_element_scrollHeight = lambda: '''
        return arguments[0].scrollHeight;
    '''
    "get the scrollHeight of the WebElement"