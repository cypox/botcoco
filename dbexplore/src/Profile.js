import React from "react";
import Accordion from "react-bootstrap/Accordion";
import "./Profile.css";
import Button from "react-bootstrap/Button";

function Profile(props) {
  return (
    <div className="col-sm-12 col-md-6 col-lg-3 mt-4">
      <Accordion defaultActiveKey="1">
        <div className="card card-main">
          <Accordion.Toggle as={Button} variant="link" eventKey="0">
            <div className="meta">
              <h5>
                {props.city}<br/>
                {props.age} ans
              </h5>
            </div>
          </Accordion.Toggle>
          <Accordion.Collapse eventKey="0">
            <div>
              {props.avatars.map((avatar) => (
                <img
                  className="card-img-top"
                  src={"http://127.0.0.1:8080/" + avatar}
                ></img>
              ))}
              <div className="card-block">
                {props.names.map((name) => (
                  <h4 className="card-title mt-3">{name.name}</h4>
                ))}
              </div>
            </div>
          </Accordion.Collapse>
        </div>
      </Accordion>
    </div>
  );
}

export default Profile;
