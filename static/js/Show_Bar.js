function mdec_tmr_bar(tm)
{
	var w=100;
	var dec=setInterval(dec_tmr_bar,tm);
	function dec_tmr_bar()
	{
		if(w<=0)
		{
			clearInterval(dec);
			document.getElementById("show_box").style.display="none";
		}
		w--;
		document.getElementById("tmr_bar").style.width=w+"%";
	}
}