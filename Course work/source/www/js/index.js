import VueSession from './vue-session/index.esm.js';

var uniqueId = function (prefix) {
  return prefix + Math.random().toFixed(13).replace(/^0\./, '')
};

var uniqueCommentId = function () {
  return uniqueId('comment-') 
}

var isInputNumber = function (value) {
  var reg = /^[\+\-]?\d*\.?\d+(?:[Ee][\+\-]?\d+)?$/;
  return reg.test(value)
}

var markInputNumber = function (element, isValid) {
  if (isValid) {
    element.style.border = "1px solid grey" 
  } else {
    element.style.border = "2px solid red" 
  }
}

Vue.prototype.$http = axios

Vue.component('login-panel', {
  props: ['isAuthorized'],
  template: `<header id="top-bar"><div id="signup-section" align="right">
              <div v-if="isAuthorized">{{ this.$session.get('display_name') }}<button v-on:click="logOut">Log Out</button></div>
              <div v-else>
              <button v-on:click="signUp">Sign Up</button><button v-on:click="logIn">Log In</button>
              <div>
    		    <label for="name"><b>Display Name</b></label>
    		    <input type="text" placeholder="Enter Display name" name="display_name" v-model="display_name" required>
    		    <br>
    		    <label for="email"><b>Email</b></label>
    		    <input type="text" placeholder="Enter Email" name="email" v-model="email" required>
				<br>
		        <label for="psw"><b>Password</b></label>
    		    <input type="password" placeholder="Enter Password" name="password" v-model="password" required>
    		  </div>
    		  </div>            
            </div></header>`,
  data: function () { return {email: '', password: '', display_name: ''} },
  methods: {
    logIn: function() {
      this.$http.post('/api/v1/user/login', {
            password: this.password,
            email: this.email
      }).then(response => {
            if (response.status === 200) {
			  this.initSession(response);
            }
          }, function (err) {
            console.log('Login error')
          })      
    },
    signUp: function () {
      this.$http.post('/api/v1/user/signup', {
            display_name: this.display_name,
            password: this.password,
            email: this.email
      }).then(response => {
            if (response.status === 200) {
              this.initSession(response);
            }
          }, function (err) {
            console.log('Signup error')
          })      
    },
    logOut: function () {
      this.$session.destroy();
      this.$root.isAuthorized = false;
    },
    initSession: function(response) {
      console.log(this);
      this.$session.start()
      this.$session.set('jwt', response.data.token)
      this.$session.set('email', this.email)              
      this.$session.set('user_id', response.data.user_id)              
      this.$session.start();      
      this.$session.set('display_name', response.data.display_name);
      this.display_name = response.data.display_name;
      this.$root.isAuthorized = true;
    },
  },
})

Vue.component('task', {
  props: ['isAuthorized'],
  template: `<div v-if="isAuthorized"><h2>Введіть список значень (лише дійсті числа)</h2>
    <div id="values">
      <input name="baseinput" type="text" v-on:input="baseInput"/>
    </div>
  </div>
  <div v-else><h2>Увійдіть щоб скористатися додатком</h2>
  </div>`,
  methods: {
    baseInput: function(e) {
      var valuesList = document.getElementById('values');
      markInputNumber(e.target, isInputNumber(e.target.value))
      if (valuesList.childElementCount === 1  && e.target.value) {
        var newInput = document.createElement('input');
        newInput.value = '';
        newInput.type = 'text';
        newInput.addEventListener('input', this.itemInput)
        valuesList.appendChild(newInput);
      }
    },
    itemInput: function(e) {
      markInputNumber(e.target, isInputNumber(e.target.value))
      var valuesList = document.getElementById('values');
      if (e.target.value) {
        if (valuesList.lastElementChild == e.target) {
          var newInput = document.createElement('input');
          newInput.value = '';
          newInput.type = 'text';
          newInput.addEventListener('input', this.itemInput)
          valuesList.appendChild(newInput);
        }
      } else {
        valuesList.removeChild(e.target)
      }
    } 
  },
})

Vue.component('comment', {
  props: ['comment', 'isAuthorized'],
  template: `
    <li>
      <span v-html="comment.text"></span>-<a :href="'/users/' + comment.user_id">{{comment.display_name}}</a>
      <span v-if="isAuthorized && this.$session.get('user_id') === comment.user_id"><button v-on:click="removeComment">Remove</button></span>
    </li>`,
  methods: {removeComment: function() {this.$root.removeComment(this.comment['id']); }
  },
})

Vue.use(VueSession)
Vue.use(VueQuillEditor)

var default_new_comment = "(enter new comment)";

var app = new Vue({
  el: '#app',
  data: {
    default_new_comment: default_new_comment,
    comment_editor: default_new_comment,
    isAuthorized: false,
  	editorOptions: {
  	  theme: 'snow',
  	  formats: ['bold', 'italic', 'underline', 'strike'],
        modules: {
          clipboard: { matchVisual: false },
          toolbar: ['bold', 'italic', 'underline', 'strike'],
        }
  	},    
  	header: "Курсова робота",
    question: "В одновимірному масиві, що складається з n елементів, обчислити середньоквадратичне значення елементів масиву.",
  	comments: [],
  },
  methods: {
    removeComment: function (comment_id) {
      axios.delete('/api/v1/comments',  { data: {'id': comment_id } }).then(response => {
          if (response.status === 200) {
            this.comments = [...response.data.comments]
          }
        }, function (err) {
          console.log('Error creating comment')
        }) 
    },
    newComment: function () {
      var text = this.comment_editor.replace(/<\/?p>|<br>/g, '')
      var user_id = this.$session.get('user_id')
      
      if (text === this.default_new_comment)
        return;
      
      this.$http.post('/api/v1/comments', { 'text': text, 'user_id': user_id }).then(response => {
          if (response.status === 200)
            this.comments = [...response.data.comments]
        }, function (err) {
          console.log('Error creating comment')
        })    
      
      this.fetchComments()
      this.comment_editor = this.default_new_comment
    },
    fetchComments: function () {
      this.$http.get('/api/v1/comments').then(response => {
          if (response.status === 200) 
            this.comments = [...response.data.comments]
        }, function (err) {
          console.log('Error fetching comments')
        })
    },
  },
  mounted: function () {
    if (this.$session.exists()) {
      this.isAuthorized = true
    }
    this.fetchComments()
  }  
})