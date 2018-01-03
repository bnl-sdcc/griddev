package gov.bnl.racf.dashboard;


import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;




public class HtmlTable
{  
    private int numColumns=0;
    private int numCells=0;

    List<HtmlTableCell> listOfCells=new ArrayList<HtmlTableCell>();

    private String tableHeader="<table border=\"BORDER\" cellpadding=\"PADDING\"  >";
    private String tableFooter="</table>";

    private int border=8;
    private int padding=8;
	
    public HtmlTable( int inputNumColumns)
	{
	    numColumns= inputNumColumns;
	}
    public void setNumColumns(int inputNumColumns)
	{
	    numColumns= inputNumColumns;
	}
    public void setBorder(int newBorder){
	border=newBorder;
    }
    public void setPadding(int newPadding){
	padding=newPadding;
    }
    public void addCell(HtmlTableCell inputCell){
	//listOfCells[numCells]=inputCell;
	numCells=numCells+1;
	listOfCells.add(inputCell);
    }
    public String toHtml(){
	String result="";
	String workTableHeader=tableHeader.replace("BORDER",Integer.toString(border));
	workTableHeader=workTableHeader.replace("PADDING",Integer.toString(padding));
	result=workTableHeader;
	result=result+"<tr>";
	int columnCounter=0;
	
	Iterator it=listOfCells.iterator();

	while(it.hasNext())
        {
          HtmlTableCell currentCell=(HtmlTableCell)it.next();
	  result=result+currentCell.toHtml();
	  columnCounter=columnCounter+1;
	  if (columnCounter==numColumns){
		columnCounter=0;
		result=result+"</tr><tr>";
	    }
        }

	result=result+tableFooter;
	return result;
    }

}

