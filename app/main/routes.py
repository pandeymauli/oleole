import os
import string
import random

from flask import session, redirect, url_for, render_template, request, flash, jsonify
from . import main
from .. import db
from .forms import CreateRoomForm, JoinRoomForm, StartStreamingForm, DropLinkForm
from wtforms.fields import RadioField
from wtforms.validators import Required
from .models import User, Room

#### HELPER FUNCTIONS #####
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_or_create_room(db_session, alias, roomLink, videoLink, team1='', team2=''):
    r = Room.query.filter_by(sharinglink = roomLink).first()
    if r:
        return r
    else:
        r = Room(sharinglink = roomLink, videoURL = videoLink, team1 = team1, team2 = team2)
        u = get_or_create_user(db_session, alias)
        r.userID = u.id
        db_session.add(r)
        db_session.commit()
        return r

def get_or_create_user(db_session, alias):
    u = User.query.filter_by(alias = alias).first()
    if u:
        return u
    else:
        u = User(alias = alias)
        db_session.add(u)
        db_session.commit()
        return u

def get_room(db_session, roomLink):
    r = Room.query.filter_by(sharinglink = roomLink).first()
    if r:
        return r.videoURL
    else:
        return None


def get_alias(db_session, alias):
    r = User.query.filter_by(alias = alias).first()
    if r:
        return r.alias
    else:
        return None


#### ROUTES #####

@main.route('/')
def index():
    return render_template('oleole.html')


@main.route('/setup', methods=['GET','POST'])
def createRoom():
    """Form to create a private room."""
    form = CreateRoomForm()
    if 'user-entered-teams' in session and session['user-entered-teams']:
        print(session['user-entered-teams'])
        print('\n\nUser entered teams\n\n')
        form.side.choices = [('1', session['user-entered-teams'][0].title()), ('2', session['user-entered-teams'][1].title()), ('0','Neutral')]
    else:
        form.side.choices = []
        redirect(url_for('.joinRoom'))

    if request.method == 'POST':
        teams = form.side.choices[:2]
        if teams:
            session['side-chosen'] = form.side.data
            session['name'] = form.name.data
            roomURL = form.name.data + '-' + id_generator() + '-' + teams[0][1].lower().replace(' ','') + '-vs-' + teams[1][1].lower().replace(' ','')
            print("Visitor of alias {} has chosen {} ".format(session['name'],session['side-chosen']))
        else:
            roomURL = form.name.data + '-' + id_generator() + '-' + 'viewing-room-link'
        session['name'] = form.name.data
        session['url'] = roomURL
        session['room'] = roomURL
        room = get_or_create_room(db.session, form.name.data, roomURL, session['videoLink'])
        session['user-entered-teams'] = []
        return redirect(url_for('.roomLink', url = roomURL))
    else:
        return render_template('y-setup.html', form=form)


@main.route('/featuredroom', methods = ['GET','POST'])
def featuredRoomSetup():
    """Form to create a featured private room."""
    ### Video Link : https://www.youtube.com/watch?v=ccp24-zhwdo
    form = CreateRoomForm()
    form.side.choices = [('1','CFC'), ('2','Neutral'),('3','MUFC')]
    if request.method == 'POST':
        teams = form.side.choices
        roomURL = form.name.data + '-' + id_generator() + '-' + teams[0][1].lower().replace(' ','') + '-vs-' + teams[2][1].lower().replace(' ','')
        session['name'] = form.name.data
        session['url'] = roomURL
        session['room'] = roomURL
        session['side-chosen'] = form.side.data
        session['videoLink'] = 'http://buffstream.com/embed/soccer.php' #'https://www.youtube.com/embed/gc3pDHSFVxU?modestbranding=1&autohide=1&showinfo=0&rel=0&autoplay=1&controls=0'
        room = get_or_create_room(db.session, form.name.data, roomURL, session['videoLink'], teams[0][1], teams[2][1])
        session['user-entered-teams'] = []
        return redirect(url_for('.roomLink', url = roomURL))
    return render_template('y-setup.html', form=form)


@main.route('/sharelink/<url>')
def roomLink(url):
    form = StartStreamingForm()
    return render_template('y-sharelink.html', url=url, form=form)


@main.route('/joinroom/<url>', methods=['GET', 'POST'])
@main.route('/joinroom', methods=['GET', 'POST'])
def joinRoom(url=''):
    """Form to enter a private room."""
    form = JoinRoomForm()
    if form.validate_on_submit() and request.method == 'POST':
        session['name'] = form.name.data
        session['side-chosen'] = form.side.data
        session['room'] = form.room.data
        print('Before querying', session['room'])
        videoURL = get_room(db.session, session['room'])
        if videoURL:
            session['room'] = form.room.data
            session['videoLink'] = videoURL
            if get_alias(db.session, session['name']):
                flash('Sorry! That alias is already taken! Try another alias')
                return redirect(url_for('.joinRoom'))
            else:
                get_or_create_user(db.session, session['name'])
                print('Form data is accurate', form.name.data, form.room.data, form.side.data)
                print('Room code is accurate', session['name'], session['room'], session['videoLink'])
                return redirect(url_for('.chat'))
        else:
            print('Room code is not accurate')
            flash('Sorry! That room code does not seem accurate')
            form.name.data = session.get('name', '')
            return redirect(url_for('.joinRoom'))
    return render_template('y-joinroom.html', form=form, url=url)


#@main.route('/viewing-room/<url>')
@main.route('/chat', methods=['GET', 'POST'])
def chat():
    """Chat room. The user's name and room must be stored in the session."""
    name = session.get('name', '')
    sideChosen = session.get('side-chosen', '')
    room = session.get('room', '')
    print(room, session['videoLink'])
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('sports-room3.html', name=name, room=room, videoURL = session['videoLink'])


@main.route('/createroom', methods=['GET','POST'])
def newRoom():
    """Create your own room"""
    form = DropLinkForm()
    if request.method == 'POST' and form.validate_on_submit():
        if str(form.team1.data.strip().lower()) and str(form.team2.data.strip().lower()):
            session['user-entered-teams'] = [form.team1.data.strip().lower(), form.team2.data.strip().lower()]
        else:
            session['user-entered-teams'] = []
        session['videoLink'] = form.videoURL.data.strip().replace('watch?v=','embed/')
        session['videoLink'] = session['videoLink'] + '?autoplay=1'
        print(session['user-entered-teams'], session['videoLink'])
        return redirect(url_for('.createRoom'))
    return render_template('y-createroom.html', form=form)
