"use strict";

const BaseUrl = "https://u9ozoz6muk.execute-api.ap-northeast-1.amazonaws.com/Prod";
const ApiKey = config.KEY;
const SECTIONS = "1H, 3H, 12H"; // From NYTimes

function buildUrl (section) {
    //return BaseUrl + url + ".json?api-key=" + ApiKey;
  let start = "-PT1H"
  let end = "P0D"
  if (section === "1H"){
    start = "-PT1H"
  }else if (section === "3H"){
    start = "-PT3H"
  }else if (section === "12H"){
    start = "-PT12H"
  }
  return BaseUrl + "?start=" + start + "&end=" + "P0D";
}

Vue.component('met-list', {
  props: ['results'],
  template: `
    <section>
      <div class="row" v-for="posts in processedPosts">
        <div class="columns large-6 medium-6" v-for="post in posts">
          <div class="card">
          <div class="card-divider">
          {{ post.StackName }}
          </div>
           <a :href="post.url" target="_blank">
          <img :src="post.image_url"></a>
          <div class="card-section">
            <p>{{ post.Resources }}</p>
          </div>
        </div>
        </div>
      </div>
  </section>
  `,
  computed: {
    processedPosts() {
      let posts = this.results;

      // Add image_url attribute
      posts.map(post => {
        // let imgObj = post.multimedia.find(media => media.format === "superJumbo");
        // post.image_url = imgObj ? imgObj.url : "http://placehold.it/300x200?text=N/A";
        let imgObj = post.Image;
        post.url = "https://ap-northeast-1.console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/stackinfo?stackId={}&filteringStatus=active&filteringText=&viewNested=true&hideStacks=false"
        post.image_url = "data:image/png;base64,"+imgObj;

        Base64ToImage(imgObj, function(img) {
          // <img>要素にすることで幅・高さがわかります
          alert("w=" + img.width + " h=" + img.height);
          // <img>要素としてDOMに追加
          document.getElementById('main').appendChild(img);
        });
      });

      // Put Array into Chunks
      let i, j, chunkedArray = [], chunk = 4;
      for (i=0, j=0; i < posts.length; i += chunk, j++) {
        chunkedArray[j] = posts.slice(i,i+chunk);
      }
      return chunkedArray;
    }
  }
});

function Base64ToImage(base64img, callback) {
  var img = new Image();
  img.onload = function() {
    callback(img);
  };
  img.src = base64img;
}

const vm = new Vue({
  el: '#app',
  data: {
    results: [],
    sections: SECTIONS.split(', '), // create an array of the sections
    section: '1H', // set default section to '1H'
    loading: true,
    title: ''
  },
  mounted () {
    this.getPosts('1H');
  },
  methods: {
    getPosts(section) {
      this.loading = true;
      let url = buildUrl(section);
      axios.get(url).then((response) => {
        this.loading = false;
        this.results = response.data.results;
        let title = this.section !== '1H' ? "Metrics in '"+ this.section + "" : "Metrics";
        this.title = title + "(" + response.data.num_results+ ")";
      }).catch((error) => { console.log(error); });
    }
  }
});
