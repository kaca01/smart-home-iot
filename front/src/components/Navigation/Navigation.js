import React, { Component } from 'react';
import './Navigation.css';
import { Navbar, NavItem, NavLink } from 'reactstrap';
import { Link } from 'react-router-dom';


export class Navigation extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <header>
                <Navbar className="navbar">
                    <ul>
                        <span className="logo">Smart Home</span>
                        <NavItem>
                            <NavLink tag={Link} className="text-light" to="/devices">PI1</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink tag={Link} className="text-light" to="/">PI2</NavLink>
                        </NavItem>
                        <NavItem className="logout">
                            <NavLink tag={Link} className="text-light" to="/">PI3</NavLink>
                        </NavItem>
                    </ul>
                </Navbar>
            </header>
        );
    }
}