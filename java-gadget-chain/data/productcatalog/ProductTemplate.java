// A stripped version of the lab's original ProductTemplate.java’s main class. Everything not needed was removed.

// The static final long serialVersionUID = 1L; variable must be set, otherwise a version number is generated
// each time a class is executed. Deserialising the same class, this flag must be set. (It is also set in the
// backend, see the original ProductTemplate.java)

package data.productcatalog;

import java.io.Serializable;

public class ProductTemplate implements Serializable {
    static final long serialVersionUID = 1L;

    private final String id;
    private transient Product product;

    public ProductTemplate(String id)
    {
        this.id = id;
    }

    public String getId() {
        return id;
    }
}