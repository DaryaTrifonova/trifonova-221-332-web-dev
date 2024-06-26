from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from models import db, Course, Category, User, Review
from tools import CoursesFilter, ImageSaver
from forms import ReviewForm

bp = Blueprint('courses', __name__, url_prefix='/courses')

COURSE_PARAMS = [
    'author_id', 'name', 'category_id', 'short_desc', 'full_desc'
]

def params():
    return { p: request.form.get(p) or None for p in COURSE_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': [x for x in request.args.getlist('category_ids') if x],
    }

@bp.route('/')
def index():
    courses = CoursesFilter(**search_params()).perform()
    pagination = db.paginate(courses)
    courses = pagination.items
    categories = db.session.execute(db.select(Category)).scalars()
    return render_template('courses/index.html',
                           courses=courses,
                           categories=categories,
                           pagination=pagination,
                           search_params=search_params())

@bp.route('/new')
@login_required
def new():
    course = Course()
    categories = db.session.execute(db.select(Category)).scalars()
    users = db.session.execute(db.select(User)).scalars()
    return render_template('courses/new.html',
                           categories=categories,
                           users=users,
                           course=course)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    f = request.files.get('background_img')
    img = None
    course = Course()
    try:
        if f and f.filename:
            img = ImageSaver(f).save()

        image_id = img.id if img else None
        course = Course(**params(), background_image_id=image_id)
        db.session.add(course)
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        categories = db.session.execute(db.select(Category)).scalars()
        users = db.session.execute(db.select(User)).scalars()
        return render_template('courses/new.html',
                            categories=categories,
                            users=users,
                            course=course)

    flash(f'Курс {course.name} был успешно добавлен!', 'success')

    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    course = db.get_or_404(Course, course_id)
    user_review = Review.query.filter_by(course_id=course_id, user_id=current_user.id).first()
    form = ReviewForm()

    if user_review:
        form = None 
    return render_template('courses/show.html', course=course, review = user_review, form = form)

@bp.route('/<int:course_id>/reviews')
def show_all_reviews(course_id):
    form = ReviewForm()
    course = db.get_or_404(Course, course_id)
    sort_order = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)

    query = Review.query.filter_by(course_id=course_id)
    if sort_order == 'positive':
        query = query.order_by(Review.rating.desc())
    elif sort_order == 'negative':
        query = query.order_by(Review.rating.asc())
    else:
        query = query.order_by(Review.created_at.desc())

    pagination = db.paginate(query, page=page, per_page=5)
    reviews = pagination.items

    return render_template('courses/reviews.html', course=course, reviews=reviews, pagination=pagination, sort_order=sort_order, form=form)

@bp.route('/<int:course_id>/reviews/new', methods=['GET', 'POST'])
@login_required
def new_review(course_id):
    form = ReviewForm()
    if form.validate_on_submit():
        rating=form.rating.data
        review = Review(
            rating=rating,
            text=form.text.data,
            course_id=course_id,
            user_id=current_user.id
        )
        db.session.add(review)
        db.session.commit()

        course = db.get_or_404(Course, course_id)
        course.rating_sum += rating
        course.rating_num += 1
        db.session.commit()
        flash('Ваш отзыв был добавлен!', 'success')
        return redirect(url_for('courses.show_all_reviews', course_id=course_id))

    return render_template('courses/show.html', form=form, course_id=course_id)