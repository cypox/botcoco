import React from "react";
import Accordion from "react-bootstrap/Accordion";
import "./Profile.css";
import Button from "react-bootstrap/Button";

function Profile(props) {
  return (
    <div className="col-sm-12 col-md-6 col-lg-4 mt-4">
      <Accordion defaultActiveKey="1">
        <div className="card">
          <Accordion.Toggle as={Button} variant="link" eventKey="0">
            <h4 className="card-title mt-3">{props.names[0].name}</h4>
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
                <div className="meta">
                  <h5>
                    {props.city}, {props.age} ans
                  </h5>
                </div>
              </div>
            </div>
          </Accordion.Collapse>
          <div className="card-footer"></div>
        </div>
      </Accordion>
    </div>
  );
}

export default Profile;
