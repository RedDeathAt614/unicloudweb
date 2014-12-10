/**
 * MailchimpController
 *
 * @description :: Server-side logic for managing mailchimps
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

module.exports = {

	subscribe: function(req,res,next){
		console.log("Subscribe:",req.params.all());

		res.view('static/index',{message: "Thank you for signing up - you're the best!"});
	}

};
