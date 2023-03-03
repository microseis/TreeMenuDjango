import logging
import logging.config

from django import template
from django.db.models import Q
from menu.models import MenuItem

logger = logging.getLogger()

logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# log to console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

register = template.Library()


def build_node(nodes: list, node: MenuItem):
    """Метод для рекурсивного сбора элементов меню и их
    абсолютных url."""
    node_path = '/'+node.menu.slug+'/'+node.url+'/'
    build_nodes(nodes, node.id)
    return node, node_path


def build_nodes(nodes: list, node_parent_id: str) -> list:
    """Метод для сбора списка отображаемых элементов меню."""
    output = []
    sub_nodes = [node for node in nodes if node.parent_id == node_parent_id]
    if len(sub_nodes) > 0:
        for sub_node in sub_nodes:
            single_output, node_paths = build_node(sub_nodes, sub_node)
            output.extend([single_output, node_paths])
        return output


@register.inclusion_tag("template_tags/menu.html", takes_context=True)
def draw_menu(context, request) -> dict:
    """Метод отображения меню."""
    slugs = context.request.get_full_path().split("/")

    logging.info("slug: {} ".format(slugs))
    try:
        menu = (
            MenuItem.objects.select_related("menu")
            .filter(Q(menu__slug__in=slugs, menu__named_url__in=slugs))
            .order_by("url")
            .distinct()
        )

        result = []
        parent_list = []
        for item in menu:
            if item.parent_id not in parent_list and (
                len(parent_list) <= len(slugs) - 2
            ):
                parent_list.append(item.parent_id)
                res = build_nodes(menu, item.parent_id)
                result.append([res])

        try:
            top_menu = menu[0]
        except IndexError:
            top_menu = menu
        return {
            "top_menu": top_menu,
            "menu_items": menu,
            "request": request,
            "nodes": result,
        }
    except MenuItem.DoesNotExist:
        logging.info("Menu does not exists")
        return {"menu": "", "request": request}
