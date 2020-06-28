var convert_timestamp = (date) => {
    myDate = date.split("-");
    var newDate = myDate[1]+"/"+myDate[0]+"/"+myDate[2];
    return new Date(newDate).getTime()

}