
App structure preparation
-------------------------

    #   props is used to have dynamic apps

    >   cd ~/PROJECTS/React/TESTS
    >   npm init react-app props-funcions
    >   cd ~/PROJECTS/React/TESTS/props-funcions
    >   mkdir src/components
    >   cd src/components
    >   touch Header.js Main.js Sidebar.js
    >   cd ~/PROJECTS/React/TESTS/props-funcions/src

App.js
------
    import Header from './components/Header';
    import Main from './components/Main';
    import Sidebar from './components/Sidebar';

    import './App.css';

    function App() {
      return (
        <div>
            <Header name="Roby" color="blue" />
            <Main greet="Greetings" />
            <Sidebar greet="Greetings" />
        </div>
      )
    }
    export default App;

Header.js
---------

    import React from "react";

    import '../App.css';

    function Header(props) {
        console.log(props)
        return (
            <div>
                Hello from Header!
                <li>{props.name}</li>
                <li>{props.color}</li>
            </div>
        )
    }
    export default Header;

Main.js
-------
    import React from "react";

    import './App.css';

    function Main(props) {
      return <h2>{props.greet}Hello from Main!</h2>
    }
    export default Main;

Sidebar.js
----------
    import React from "react";

    import './App.css';

    function Sidebar(props) {
      return <h2>{props.greet}Hello from Sidebar!</h2>
    }
    export default Sidebar;
---
    >   cd ~/PROJECTS/React/TESTS/props-funcions
    >   npm start