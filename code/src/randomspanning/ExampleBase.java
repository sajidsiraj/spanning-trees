/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package randomspanning;


/**
 *
 * @author busssir
 */
public abstract class ExampleBase {
    String _name="unknown";
    public String getName(){return _name; };
    
    public abstract PC get_top();
    public abstract PC getPCM(int id);
 
    public static PC createPC(int n){
        PC c = new PC(n);
        for( int i=0; i<c.n(); i++ ){
            for( int j=0; j<c.n(); j++ ){ c.set(i, j, -1); }
            c.set(i, i, 1);
        }
        return c;
    }

}
