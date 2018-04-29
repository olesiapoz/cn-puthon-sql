function Tweet(data) { 
    this.id = ko.observable(data.id); 
    this.username = ko.observable(data.tweetedby); 
    this.body = ko.observable(data.body); 
    this.timestamp = ko.observable(data.timestamp); 
  } 

  function TweetListViewModel() { 
    var self = this; 
    self.tweets_list = ko.observableArray([]); 
    self.username= ko.observable(); 
    self.body= ko.observable(); 

    self.addTweet = function() { 
    self.save(); 
    self.username(""); 
    self.body(""); 
     }; 

    $.getJSON('/api/v2/tweets', function(tweetModels) { 
    var t = $.map(tweetModels.tweets_list, function(item) { 
      return new Tweet(item); 
    }); 
    self.tweets_list(t); 
    }); 

   self.save = function() { 
    var new_tweet = new Tweet({username: self.username(), body: self.body()})
    return $.ajax({ 
    url: '/api/v2/tweets', 
    contentType: 'application/json', 
    type: 'POST', 
    data: JSON.stringify({ 
       'username': self.username(), 
       'body': self.body(), 
    }), 
    success: function(data, status, jq) { 
       alert("success") 
            console.log("Pushing to users array"); 
            self.tweets_list.push(new_tweet); 
            return; 
    }, 
    error: function() { 
       return console.log("Failed"); 
    } 
   }); 
    }; 
  } 

 ko.applyBindings(new TweetListViewModel()); 