import React, { Component } from 'react';
import './Navigation.css';
import { Navbar, NavItem, NavLink } from 'reactstrap';
import { Link } from 'react-router-dom';


export class Navigation extends Component {
    constructor(props) {
        super(props);
    }

    handlePiClick = (pi) => {
        this.props.updateSelectedPi(pi);
    }

    render() {
        return (
            <header>
                <Navbar className="navbar">
                    <ul>
                        <span className="logo">Smart Home</span>
                        <NavItem>
                            <NavLink onClick={() => this.handlePiClick("PI1")} tag={Link} className="text-light" to="/devices">PI1</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink onClick={() => this.handlePiClick("PI2")} tag={Link} className="text-light" to="/">PI2</NavLink>
                        </NavItem>
                        <NavItem className="logout">
                            <NavLink onClick={() => this.handlePiClick("PI3")} tag={Link} className="text-light" to="/">PI3</NavLink>
                        </NavItem>
                    </ul>
                </Navbar>
            </header>
        );
    }
}