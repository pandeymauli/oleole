from flask import session, redirect, url_for, render_template, request, flash
from . import main
from .forms import CreateRoomForm, JoinRoomForm, StartStreamingForm


@main.route('/')
def hom():
    return render_template('home.html')

@main.route('/create-room', methods=['GET','POST'])
def createRoom():
    """Login form to enter a room."""
    form = CreateRoomForm()
    if form.validate_on_submit() and request.method == 'POST':
        teams = form.side.choices[:2]
        roomURL = form.name.data + '-' + teams[0][1].lower().replace(' ','') + '-vs-' + teams[1][1].lower().replace(' ','')
        session['name'] = form.name.data
        session['side'] = form.side.data
        session['url'] = roomURL
        session['room'] = roomURL
        print("Visitor of alias {} has chosen {} ".format(session['name'],session['side']))
        return redirect(url_for('.roomLink', url = roomURL))
    elif request.method == 'POST':
        flash('Looks like you missed a field there! Fill both fields and resubmit!')
        form.name.data = session.get('name', '')
        form.side.data = session.get('side', '')
        return render_template('create-room.html', form=form)
    else:
        return render_template('create-room.html', form=form)

@main.route('/join-room', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = JoinRoomForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)

@main.route('/create-room/<url>')
def roomLink(url):
    form = StartStreamingForm()
    return render_template('streaming.html', url=url, form=form)


#@main.route('/viewing-room/<url>')
@main.route('/chat', methods=['GET', 'POST'])
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('sports-room.html', name=name, room=room)
