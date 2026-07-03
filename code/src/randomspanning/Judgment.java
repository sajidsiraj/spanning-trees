/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package randomspanning;

public class Judgment{
    public int id;
    public int i;
    public int j;
    public double a;
    public boolean used;
    public Judgment(int idd, int ii, int jj, double aa){
        id = idd; i=ii; j=jj; a=aa;
        used=false;
    }
    public String hash(){
        return hash(i,j);
    }
    public static String hash(int i, int j){
        return (i>j)?"a"+i+""+j:"a"+j+""+i;
    }
}
