from flask import Flask, render_template, request
from pony.orm import db_session, select
from database import Video

app = Flask(__name__)

@app.route('/')
@db_session
def index():
    q = request.args.get('q', '').lower()
    category = request.args.get('category', '').lower()
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    all_videos = list(Video.select())
    
    filtered = [
        v for v in all_videos
        if q in v.name.lower() and (category in v.category.lower() if category else True)
    ]

    # Paginate the filtered list
    videos = filtered[offset:offset + per_page]
    total_pages = (len(filtered) + per_page - 1) // per_page

    categories = list(set(v.category for v in all_videos))

    return render_template(
        'index.html',
        videos=videos,
        q=q,
        category=category,
        categories=categories,
        page=page,
        total_pages=total_pages
    )


@app.route('/category/<category_name>')
@db_session
def videos_by_category(category_name):
    lower_category = category_name.lower()
    all_videos = list(Video.select())
    videos = [v for v in all_videos if v.category.lower() == lower_category]
    categories = list(set(v.category for v in all_videos)) 
    return render_template(
        'index.html',
        videos=videos,
        category=category_name,
        categories=categories,
        page=1,
        total_pages=1
    )

@app.route('/video/<int:video_id>')
@db_session
def video_detail(video_id):
    video = Video.get(id=video_id)

    if video is None:
        return "Video not found", 404

    category = video.category
    all_videos = list(Video.select().filter(category=category))

    seen_ids = set()
    related = []
    for v in all_videos:
        if v.id != video.id and v.id not in seen_ids:
            related.append(v)
            seen_ids.add(v.id)
        if len(related) >= 15:
            break
    print("Related video IDs:", [v.id for v in related])
    return render_template('video.html', video=video, related=related)

if __name__ == '__main__':
    app.run(debug=True)
