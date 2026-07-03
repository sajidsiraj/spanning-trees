/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package randomspanning;
/**
 *
 * @author sirajs
 */
public abstract class Method {
    Method(String name){_name=name;}
    public String getName() { return _name; }

    public abstract Result[] doCalculate(PC A);

    String      _name = "...";
    PC         _A;
    Result[]    _vW;

}
