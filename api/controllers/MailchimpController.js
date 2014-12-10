/**
 * MailchimpController
 *
 * @description :: Server-side logic for managing mailchimps
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

var MCapi = require('mailchimp-api');
MC        = new MCapi.Mailchimp('4cf0247d56b6ff76096779ab80b712b9-us9');

module.exports = {

	subscribe: function(req,res,next){

		var listID = "288eb7197d"; // (Betalist list)
		MC.lists.subscribe({id: listID, email:{email:req.body.email}}, function(data) {
			res.view('static/index',{message: "Thank you for signing up - you're the best!"});
		},
		function(error) {
			var errText = '';
			if (error.error) {
				//req.session.error_flash = error.code + ": " + error.error;
				errText = error.error;
			} else {
				//req.session.error_flash = 'There was an error subscribing that user';
				errText = 'There was an error subscribing that user';
			}
			res.view('static/index',{message: errText});
		});

	}

};
