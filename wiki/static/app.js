// Create an event listener for the DOM to ensure DOM is loaded before manipulation 
document.addEventListener( 'DOMContentLoaded', function(){

// Search Pages Based on user input and clear searches if input is empty 
// Use a debounce function to delay the appending of results to create a more fluid user experience 
function debounce(func, delay) {
    let timer;
    return function() {
      clearTimeout(timer);
      timer = setTimeout(() => {
        func.apply(this, arguments);
      }, delay);
    };
  }
  
  if (search_input) {
    search_input.addEventListener('input', debounce(function() {
      let term = search_input.value;
      if (term === '') {
        console.log(term);
        clear_searches();
      } else {
        search_pages(term);
      }
    }, 250)); 
  }
  
});

// Create Search Results Based on user input and append those results to the page 
const SEARCH_PAGES_BASE = 'https://en.wikipedia.org/w/rest.php/v1/search/page?';
const SEARCH_PAGE_BASE = 'https://en.wikipedia.org/w/rest.php/v1/page/';
const container = document.getElementById( 'results' )
const search_form = document.getElementById( 'search-pages-form' )
const search_input = document.querySelector( '[name = "search_input"]' )


// Search Pages Async Function / Recieve results and pass to the append function
const search_pages = async( term ) => {
    const res = await axios.get( `${ SEARCH_PAGES_BASE }q=${ term }&limit=25` );
    const data = res.data;
    const pages = data.pages;
    clear_searches();
    for( let page of pages ){
        if( page.thumbnail ){
            append_pages( page.title, page.description, page['thumbnail']['url'] )
        }
        else{
            append_pages( page.title, page.description )
        }
    }

    const div = document.querySelectorAll( '[class = "form-control border border-info fs-5 text-center text-white bg-dark"]' );
    for( let d of div ){

    d.addEventListener( 'mouseover', function(){
        d.setAttribute( 'class', 'form-control border border-black fs-5 text-center bg-info' );
    });

    d.addEventListener( 'mouseleave', function(){
        d.setAttribute( 'class', 'form-control border border-info fs-5 text-center text-white bg-dark' );
    });
    }
}

// Append the search results to the page 
const append_pages = ( title, description, thumbnail ) => {
    const a = document.createElement( 'a' );
    const div = document.createElement( 'div' );
    const p = document.createElement( 'p' );
    const h1 = document.createElement( 'h1' );
    const img = document.createElement( 'img' );
    
    div.setAttribute( 'class', 'form-control border border-info fs-5 text-center text-white bg-dark' );
    a.setAttribute( 'href', `http://127.0.0.1:5000/get-page/${ title }`);
    a.setAttribute( 'class', 'text-decoration-none text-center' );
    if( thumbnail ){
        img.setAttribute( 'src', thumbnail );
        img.setAttribute( 'width', '60px' );
        img.setAttribute( 'class', 'mx-3 rounded' );
    }

    h1.innerText = title;
    h1.append( img );
    p.innerText = description;
    div.append( h1, p );
    a.append( div );
    container.append( a );
}

// Clears searches if search input is empty 
const clear_searches = () => {
    container.innerHTML = '';
    return container;
}

const div = document.querySelectorAll( '[class = "form-control border border-info fs-5 text-center text-white bg-dark"]' );

for( let d of div ){
    d.addEventListener( 'mouseover', function(){
        d.setAttribute( 'class', 'form-control border border-black fs-5 text-center bg-info' );
    })

    d.addEventListener( 'mouseleave', function(){
        d.setAttribute( 'class', 'form-control border border-info fs-5 text-center text-white bg-dark' );
    })
}

// Format the Appended HTML Page 
if( document.getElementById( 'page' )){
    const html = document.getElementById( 'page' );
    html.innerHTML = html.innerText;
}

const base = document.getElementsByTagName('base')
for ( let i of base ) {
    i.setAttribute('href', 'http://127.0.0.1:5000/')
}

// Search History Page Animation 
const searchAnchorContainer = document.querySelectorAll( '[ id = "search-anchor-container" ]' );
const searchHistoryItemDivs = document.querySelectorAll( '[id="search-history-item-div"]' );
const searchHistoryItemP = document.querySelectorAll( '[id="search-history-item-p"]' );
const searchHistoryButtons = document.querySelectorAll( '[id="search-history-button"]' );
console.log( searchAnchorContainer );
console.log( searchHistoryItemDivs );
console.log( searchHistoryItemP );
console.log( searchHistoryButtons );


for ( let div of searchHistoryItemDivs ){
    div.addEventListener( 'mouseover', function(){
        div.firstChild.classList.remove( 'text-white' );
        div.firstChild.classList.add( 'text-dark' );
        div.classList.remove( 'bg-dark', 'form-control', 'fs-5', 'text-center' );
        div.classList.add( 'bg-info', 'form-control', 'fs-5', 'text-center', 'text-black' );
        for( let p of searchHistoryItemP ){
            if( p.parentElement === div ){
                p.lastElementChild.classList.remove( 'btn-outline-info' );
                p.lastElementChild.classList.add( 'btn-outline-dark' );
            }
        }
    });

    div.addEventListener( 'mouseleave', function(){
        div.classList.remove( 'bg-info', 'form-control', 'fs-5', 'text-center', 'text-black' );
        div.classList.add( 'bg-dark', 'form-control', 'fs-5', 'text-center' );
        for( let p of searchHistoryItemP ){
            if( p.parentElement === div ){
                p.lastElementChild.classList.remove( 'btn-outline-dark' );
                p.lastElementChild.classList.add( 'btn-outline-info' );
            }
        }
    });
}
 
//


