<template>
  <div :class="['video-player', placeholder]">
    <div
      v-if="videoLoadError"
      :width="ytprefs.width"
      :height="ytprefs.height"
      class="fill">
      {{ videoLoadError.message }}
    </div>
    <div
      v-if="activeVideo && activeVideo.video_id"
      :class="[ 'video-container', placeholder ]">
      <youtube
        ref="youtube"
        :class="placeholder"
        :video-id="activeVideo.video_id"
        :width="ytprefs.width"
        :height="ytprefs.height"
        :player-vars="playerVars" />

      <div class="row">
        <h3>{{ activeVideo.title|truncate(65) }}</h3>
      </div>
      <div v-if="!user.loggedIn">
        <div v-if="loginError">
          <h3>Error logging in!</h3>
          <p>
            {{ loginError.message }}
          </p>
        </div>
        <div v-else-if="logoutError">
          <h3>Error logging out!</h3>
          <p>
            {{ logoutError.message }}
          </p>
        </div>
        <div v-else>
          <h3>Please Log In to see and track chat messages</h3>
          <div>
            <button class="btn btn-blue" @click="authenticate ('google')">Login With Google</button>
          </div>
        </div>
      </div>
      <div v-else>
        <div style="float:left" class="w-1/4">
          <img 
            :src="user.avatar" 
            height="100" 
            width="100">
          <br clear="left">
          <button class="btn btn-red" @click="doLogout()">Log Out</button>
          <br clear="left">
          <em>Welcome,</em>
          <br>
          <em>{{ user.name }}</em>
        </div>
        <div style="padding: 20px 20px 20px 20px; float:right" class="w-3/4 shadow-lg rounded bg-grey-lightest border border-grey items-center">
          <p v-if="!user.loggedIn" class="text-sm text-grey-dark flex">
            <svg class="fill-current text-grey w-3 h-3 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <path d="M4 8V6a6 6 0 1 1 12 0v2h1a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-8c0-1.1.9-2 2-2h1zm5 6.73V17h2v-2.27a2 2 0 1 0-2 0zM7 6v2h6V6a3 3 0 0 0-6 0z" />
            </svg>
            Chat for logged in members only 
          </p>
          <ul class="overflow-x-auto overflow-hidden border border-grey text-sm m-0 px-8 py-4  items-center" style="height: 70vh;" v-chat-scroll>
            <li
              v-for="message in filteredMessages"
              :key="message.snippet.id">
              <p class="text-sm text-grey-dark">
                <em style="color:red">{{message.authorDetails.name}}</em>:
                {{message.snippet.message}}
              </p>
            </li>
          </ul>            
            <input v-model="messageFilter" 
            class="mt-2 w-1/2 px-3 py-2 border border-grey" 
            type="text"
              placeholder="Filter by name" 
              style="margin-bottom:20px"
              @keydown.enter="sendMessage"/>
              <button class="btn btn-red" @click=clearMessageFilter()>
                clear
              </button>
        </div>
      </div>
    </div>
    <div :class="[ 'video-list', placeholder ]">
      <div
        v-for="video in videos"
        :key="video.video_id"
        class="thumbnail"
        @click="chooseVideo(video)">
        <div class="thumbnail-img">
          <img
            :src="video.thumbnail.url"
            :height="video.thumbnail.height"
            :width="video.thumbnail.width"
            alt="Play Video">
        </div>
        <div class="thumbnail-info">
          <em>{{ video.title }}</em>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  // 
  import axios from 'axios'
  import preloadVideos from './preloadVideos'

  const loggedOutUser = {
          name: null,
          avatar: null,
          loggedIn: false,
          token: null,
          refreshToken: null
        }
  const apiRoot = 'http://www.tasq.us/api/v1'

  export default {
    name: 'VideoPlayer',
    data() {
      return {
        playerVars: { autoplay: false },
        videosLoading: true,
        videos: preloadVideos,
        videoLoadError: null,
        selectedVideo: null,
        selectedChat: null,
        loginError: null,
        logoutError: null,
        userLoading: false,
        chatError: null,
        user: this.$_.clone(loggedOutUser),
        ytprefs: {width: 800, height: undefined},
        messages: [],
        message: "",
        messageFilter: null,
        timeoutId: null,
        endpoints: {
            validateToken: `${apiRoot}/auth/authorized`,
            logout: `${apiRoot}/auth/logout`,
            refresh: `${apiRoot}/auth/refresh`,
            me: `${apiRoot}/users/me`,
            liveVideos: `${apiRoot}/ytlive/live?search=fortnite&max=5`,
            liveChatInfo: `${apiRoot}/ytlive/videos/--videoid--/live_chat`,
            liveChatMessages: `${apiRoot}/ytlive/live_chats/--chatid--/messages`
          }        
      }
    },
    computed: {
      placeholder: function() {
        return this.videosLoading ? " placeholder" : ""
      },
      activeVideo: function() {
        if(this.selectedVideo)
          return this.selectedVideo;
        if(this.videos && this.videos.length)
          return this.videos[0]
        return null
      },
      filteredMessages: function() {
        if(this.messageFilter) {
          const filter = this.messageFilter
          return this.messages.filter(function(message) {
            return message.authorDetails.name.toUpperCase().startsWith(filter.toUpperCase())
          })
        } else {
          return this.messages
        }
      },
      rowStyle: function(on) {
        return on ? '#DDD' : '#2c3e50'
      }
    },
    beforeMount() {
      this.loadVideosAndCheckToken()
    },
    methods: {
      loadVideosAndCheckToken: function() {
        const vm = this
        try { // catch any uncaught non-async exceptions
          vm.loginWithCookie()
          vm.loadLiveVideos()
        }  catch(error) {
          // We really want the finally
        }  finally {
          vm.videosLoading = false
        }
      },
      chooseVideo: function(video) {
        const vm = this
        this.selectedVideo = video
        const url = this.endpoints['liveChatInfo'].replace('--videoid--', video.video_id)
        axios.get(url).then( (response) => {
          vm.selectedChat = response.data
          vm.chatRunner()
        })
        .catch( (error) => {
          vm.chatError = error
        })
      },
      clearMessageFilter: function() {
        this.messageFilter = null
      },
      chatRunner: function() {
        const vm = this
        vm.timeoutId = null
        const chatId = this.selectedChat.chat_id
        const chatUrl = this.endpoints['liveChatMessages'].replace('--chatid--', chatId)
        function listMessages(vm, chatId, nextToken, delay) {
          vm.timeoutId = setInterval( function(chatId, nextToken){
            axios.post(chatUrl, { nextToken: nextToken})
            .then(function(response) {
              const items = response.data.items
              vm.messages.push(...items)
              clearInterval(vm.timeoutId)

              listMessages(
                  vm,
                  chatId, 
                  response.data.nextPageToken,
                  response.data.pollingIntervalMillis                  
                )      
            })
            .catch(function(error) {
              clearInterval(vm.timeoutId)
              vm.chatError=error
            })
          }, delay)      
        }
        listMessages(vm, chatId, null, 0)
      },
      sendMessage(message) {
        this.messages.push(this.user.name + ": " + message)
      },
      authenticate: function() {
        window.location.href = 'http://www.tasq.us/api/v1/auth/login'
      },
      doLogout: function() {
        const vm = this
        window.$cookies.remove('refresh_token')
        if(this.user.token) {
          axios.delete(vm.endpoints['logout'])
            .catch( function(error) {vm.logoutError = error })
        }
        axios.defaults.headers.common = {'X-API-KEY': 'Bearer ' + vm.user.token}
        vm.user = this.$_.clone(loggedOutUser)
      },
      loginWithCookie: function() {
        var vm = this

        const token = window.$cookies.get('access_token')
        const refreshToken = window.$cookies.get('refresh_token')

        if(!token && refreshToken) {
          axios.defaults.headers.common = {'X-API-KEY': 'Bearer ' + refreshToken}

          const refresh = vm.endpoints['refresh']
          axios.post(refresh)
            .then(function(response) {
              vm.verifyToken(response.data)
            }).catch(function(error) {
              vm.loginError = error
              vm.doLogout()
            })
        } else if(token) {
          // remove cookies and store refresh token in localStorage
          window.$cookies.remove('access_token')
          vm.verifyToken(token)
        } else {
          vm.doLogout()
        }
      },
      verifyToken: function(token) {
        const vm = this
        axios.defaults.headers.common = {'X-API-KEY': 'Bearer ' + token}
        axios.post(vm.endpoints['validateToken'])
          .then( function() { return axios.get(vm.endpoints['me']) })
          .then( (response) => {
            // store user info
            vm.user.name = response.data.name
            vm.user.avatar = response.data.avatar
            vm.user.token = token
            vm.user.loggedIn = true
            vm.loginError = false;
          }).catch( function(error) {
            vm.loginError = error
            // logs out if token, but always sets logged out
            vm.doLogout()
          })
      },
      loadLiveVideos: function() {
        const vm = this
        axios.get(vm.endpoints['liveVideos']).then( (response) => {
          const respVideos = response.data
          vm.videos = respVideos
          vm.videoLoadError = null
          vm.chooseVideo(this.activeVideo)
        })
        .catch( function(error) {vm.videoLoadError = error  })
        .finally( function() {vm.videosLoading = false })
      }
    }
  }
</script>

<style src="./style.css" scoped>

</style>
