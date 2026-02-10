

    ------------------------------------------------------------------------------------------------
    #   Task Requirements

    Simple typography-focused layout for a coding blog, no use of images.
    Following sections for the layout:  
    Main navigation 
    Promo (main advertisement)
    A list of newest posts' previews (intros)
    The footer 
    ------------------------------------------------------------------------------------------------

App structure preparation
-------------------------

    >   cd ~/PROJECTS/React
    >   npm init react-app customizing-example                                  #   react app creation
    >   cd customizing-example/src
    >   mkdir components                                                        #   Components folder creation
    >   cd components
    >   touch Nav.js Promo.js Intro1.js Intro2.js Intro3.js Footer.js           #   Components modules creation

Building Components
-------------------


Nav.js
------
    function Nav() {
        return (
            <nav className="main-nav">
                <ul>
                    <li>Home</li>
                    <li>Articles</li>
                    <li>About</li>
                    <li>Contact</li>
                </ul>
            </nav>
        );
    };

    export default Nav;

Promo.js
--------
    function Promo() {
        return (
            <div className="promo-section">
                <div>
                    <h1>Don't miss this deal!</h1>
                    </div>
                    <div>
                    <h2>Subscribe to my newsletter and get all the shop items at 50% off!</h2>
                </div>
            </div>
        );
    };

    export default Promo;

Intro1.js
---------
    function Intro1() {
        return (
            <div className="blog-post-intro">
                <h2>I've become a React developer!</h2>
                <div>
                    <p>I've completed the React Basics course and I'm happy to announce that I'm now a Junior React Developer!</p>
                    <p className="link">Read more...</p>
                </div>
            </div>
        );
    };

    export default Intro1;

Intro2.js
---------
    function Intro2() {
        return (
            <div className="blog-post-intro">
                <h2>Why I love front-end web development</h2>
                <div>
                    <p>In this blog post, I'll list 10 reasons why I love to work as a front-end developer.</p>
                    <p className="link">Read more...</p>
                </div>
            </div>
        );
    };
    
    export default Intro2;

Intro3.js
---------
    function Intro3() {
        return (
            <div className="blog-post-intro">
                <h2>What's the best way to style your React apps?</h2>
                <div>
                    <p>There are so many options to choose from. Here's a high-level overview of the popular ones.</p>
                    <p className="link">Read more...</p>
                </div>
            </div>
        );
    };

    export default Intro3;

Footer.js
---------
    function Footer() {
        return (
            <div className="copyright">
                <p>Made with love by Myself</p>
            </div>
        );
    };

    export default Footer;

Creating & Importing components
-------------------------------

    >   cd ~/PROJECTS/React/customizing-example/src
    >   touch Headings.js

React/customizing-example/src/Headings.js
-----------------------------------------
    function Heading () {
        return (
          <h1>Heading title in Headings.js separated file</h1>
        );
    }

    export default Heading;

    >   import Heading from './Headings';                       #   Import the Heading component into the App component.

insert the Heading JSX element in the return statement of the App component

React\customizing-example\src\App.js
------------------------------------
    import logo from './logo.svg';
    import './App.css';

    import Heading from './Headings';                               #   <===

    function App() {
      return (
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <p>
              External components loading ...
            </p>
            <span><Heading /></span>                                #   <===
          </header>
        </div>
      );
    }

    export default App;

    >   cd ~/PROJECTS/React/customizing-example
    >   npm start
