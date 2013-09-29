function rate_item(item_id, value, callback) {

    data = {
        item_id : item_id,
        value   : value,
    };
    var serializedData = JSON.stringify(data);
    Dajaxice.ratings.rate_item(Dajax.process, {'data': serializedData});

    callback(item_id, value);
}