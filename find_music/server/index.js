const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')
const db = require('./db')
const cheerio = require('cheerio');
const got = require('got');

const app = express()
const apiPort = 3000

app.use(bodyParser.urlencoded({ extended: true}))
app.use(cors())
app.use(bodyParser.json())


db.on('error', console.error.bind(console, 'MongoDB connection error:'))

app.get('/', (req, res) => {
    res.send('Hello World!')
})

const vgmUrl = 'https://pitchfork.com/reviews/albums/?genre=rap';



// (async () => {
//     const response = await got(vgmUrl);
//     const $ = cheerio.load(response.body);
//     console.log($(".review").text())
  
    
// })();

// (async () => {
//     const response = await got(vgmUrl);
//     const $ = cheerio.load(response.body);
//     console.log($(".review"))
  
    
// })();

(async () => {
    const response = await got(vgmUrl);
    const $ = cheerio.load(response.body);
    
    const mylink = $('.review').map((i, review) => {
        return {
          artist: $(review).find('.artist-list review__title-artist').,
          album: $(review).find('.review__title-album').text(),
          href: $(review).find('a').attr('href'),
        }
      }).get()
    
      console.log(mylink)
  
    
})();

// (async () => {
//     const response = await got(vgmUrl);
//     const $ = cheerio.load(response.body);
    
//     const mylink = $('.artist-list review__title-artist').map((i, title) => {
//         return {
//           artist: $(title).find('.review__title-album').find('li').text(),
//         }
//       }).get()
    
//       console.log(mylink)
  
    
// })();


// $('.review').map((i, card) => {
//     return {
//       link: $(card).find('a').text(),
//       href: $(card).find('a').attr('href'),
//     }
//   }).get()



// $(".intro")

// got(vgmUrl).then(response => {
//     const $ = cheerio.load(response.body);
  
//     $('a').each((i, link) => {
//       const href = link.attribs.href;
//       console.log(href);
//     });
//   }).catch(err => {
//     console.log(err);
//   });

app.listen(apiPort, () => console.log(`Server running on port ${apiPort}`))

