"""
Hanwei Wang
Time: 8-3-2020 15:07
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

from flask import Blueprint, render_template, flash
from Webapp.models import Post, Category

category_bp = Blueprint('category', __name__)

@category_bp.route("/")
def category():
    pass