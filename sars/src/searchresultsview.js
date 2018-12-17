import React, { Component } from 'react';
import './App.css';
import Star from './star.png';


class SearchResultsView extends Component {

   constructor(props) {
    super(props);
    this.state = {showTopics: false};
    this.toggleTopic = this.toggleTopic.bind(this);
  }

  getSentiment() {
  	let sentiment = this.props.item.sentiment.substring(0, 4);
  	let sentimentScore = parseFloat(sentiment);
  	let classname = "positive";
  	if (sentimentScore <= 0.6 && sentimentScore >= 0.4) {
  		classname = "neutral";
  	} else if (sentimentScore < 0.4) {
  		classname = "negative";
  	}

  	return {
  		score: sentimentScore,
  		style: classname
  	}
  }

  getStar(starCount) {
     let stars = []
     for (let index = 0; index < starCount; index++) {
        stars.push(<img src={Star} className="star" alt="star" key={"img"+index} />);
      }
      return stars;
  }

  getStars() {
    let stars = this.props.item.averageUserRating;
    let rcounts = this.props.item.reviewCount;
    if (stars) {
      let starCount = parseFloat(stars);
      return (
         <div className="ratingcontainer">
          <span className="ratings">Average rating by <b>{rcounts}</b> people </span> 
          <span className="starcontainer"> {this.getStar(starCount)} </span>
          </div>
        );
    } else {
      return null;
    }
  }

  toggleTopic(event) {
      let newState = !this.state.showTopics;
      this.setState({showTopics: newState});
  }

  renderTopics() {
    let topicLabel = this.state.showTopics ? "Hide topics" :  "Show topics";
    let rstyle = this.state.showTopics ? "rendertopics" :  "hidetopics";
    let topics = this.props.item.topics.join(", ");
    return (
      <div className="businesstopics">  
        <div className="topicLabel" onClick={this.toggleTopic}> {topicLabel} </div>
        <div className={rstyle}> {topics} </div>
      </div>
    );
  }

  render() {
  	let sentimentData = this.getSentiment();	
  	return (      
  		<div className="searchview">
  			<div className="businessData">
	  			<div className="businessName">{this.props.item.name}</div>
	  			<div className="addressName">{this.props.item.address}, {this.props.item.city}, {this.props.item.state}</div>
          {this.getStars()}
	  		</div>
  			<div className="sentimentData">  				
  				Sentiment score
  				<div className={sentimentData.style}>{sentimentData.score}</div>  				
  			</div>                  
          
      </div>
  	);
  }

}


export default SearchResultsView;