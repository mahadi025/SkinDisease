import tensorflow as tf
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import os
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, login_required
from forms import *
import os
from werkzeug.utils import secure_filename
from config import *
from db import *

app, __,model = start()

def contrast_adjustment(img, alpha=1.2, beta=1):
    output = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return output


@app.route('/register', methods=['GET', 'POST'])
def registration():
    if not 'logged_in' in session:
        form = UserRegistrationLoginForm()
        if request.method == 'POST':
            name = request.form['name']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password1']
            confirm_password = request.form['password2']
            if password != confirm_password:
                flash('Passwords do not match')
                return redirect(url_for('registration'))
            if User.objects(username=username) or User.objects(email=email):
                flash('Username or email already exists')
                return redirect(url_for('registration'))
            user = User(username=username, name=name,email=email,
                        password=generate_password_hash(password))
            user.save()
            return redirect(url_for('login'))
        return render_template('registration.html', form=form)
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_active:
        return redirect(url_for('home'))
    else:
        form = UserLoginForm()
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.objects.get(username=username)
            if user and check_password_hash(user['password'], password):
                login_user(user)
                session['logged_in'] = True
                user.is_active = True
                user.is_anonymous=False
                user.save()
                return redirect(url_for('home'))
            else:
                flash('Username or Password is incorrect')
        return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_active:
        user=User.objects.get(username=current_user.username)
        user.is_active=False
        user.save()
    session.clear()
    return redirect(url_for('home'))

@app.route('/view_profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    user=User.objects.get(username=current_user.username)
    return render_template('view_profile.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user=User.objects.get(username=current_user.username)
    form = UserEditForm(obj=user)
    if request.method == "POST":
        form.populate_obj(user)
        return redirect(url_for('view_profile'))

    return render_template('edit_profile.html', user=user, form=form)

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
   form=ClassifyDisease()
   if request.method == 'POST':
      # diseases_name = [
      # 'Acne', 
      # 'Acnetic Keratosis', 
      # 'Basal Cell Carcinoma', 
      # 'Capillaritis', 
      # 'Eczema', 
      # 'Folliculitis', 
      # 'Impetigo', 
      # 'Keloids', W
      # 'Lichen Planus', 
      # 'Orf', 
      # 'Psoriasis', 
      # 'Rosacea', 
      # 'Scabies', 
      # 'Skin Tag', 
      # 'Syphilis', 
      # 'Tuberous Sclerosis', 
      # 'Varicella', 
      # 'Vitiligo']
      
    #   diseases_name=[
    #      'Acne',
    #      'Eczema',
    #      'Keloids', 
    #      'Psoriasis', 
    #      'Skin Tag'
    #   ]
      diseases_name=[
         'মুখকোষ্ঠ /ব্রণ',
         'একজেমা/পামা/বিখাউজ',
         'কেলোইড',
         'সোরিয়াসিস',
         'স্কিন ট্যাগ',
        ]
      try:
         file = request.files['imageFile1']
         file_name = secure_filename(file.filename)
         file.save(f'media/images/{file_name}')
      except:
         file = request.files['imageFile2']
         file_name = secure_filename(file.filename)
         file.save(f'media/images/{file_name}')

      img=cv2.imread(f'media/images/{file_name}')
      img=contrast_adjustment(img)
      resized_img=tf.image.resize(img, (224, 224))
      cv2.imwrite(os.path.join('media', 'images',file_name ), img)
      predictions=model.predict(np.expand_dims(resized_img, 0))
      idx = predictions.argmax()
      label = f'Predicted Skin Disease: {diseases_name[idx]}'
      return render_template('index.html', prediction=label, img=file_name, current_user=current_user, form=form)
   else:
      return render_template('index.html', form=form)

if __name__ == '__main__':
   login_manager.init_app(app)
   app.run(host='127.0.0.1', port=5001, debug=True)